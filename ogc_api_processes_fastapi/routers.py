# Copyright 2022, European Union.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import urllib.parse
from typing import Any

import fastapi

from . import clients, models


def create_get_processes_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /processes` endpoint
    as implemented by `client`.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /processes` endpoint.
    """

    @router.get(
        "/",
        response_model=models.ProcessesList,
        response_model_exclude_none=True,
        summary="retrieve the list of available processes",
        operation_id="getProcesses",
    )
    def get_processes(
        request: fastapi.Request,
        limit: int = fastapi.Query(default=10, ge=1, le=100),
        offset: int = fastapi.Query(default=0, ge=1),
    ) -> models.ProcessesList:
        """The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process_list = client.get_processes_list(limit=limit, offset=offset)
        for process_summary in process_list:
            process_summary.links = [
                models.Link(
                    href=urllib.parse.urljoin(
                        str(request.base_url), f"processes/{process_summary.id}"
                    ),
                    rel="self",
                    type="application/json",
                    title="process description",
                )
            ]
        links = [
            models.Link(
                href=urllib.parse.urljoin(str(request.base_url), "processes/"),
                rel="self",
            )
        ]
        processes_list = models.ProcessesList(processes=process_list, links=links)

        return processes_list


def create_get_process_description_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /processes/{process_id}` endpoint
    as implemented by `client`.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /processes/{process_id}` endpoint.
    """

    @router.get(
        "/{process_id}",
        response_model=models.ProcessDescription,
        response_model_exclude_none=True,
        response_model_exclude_unset=True,
        summary="retrieve the description of a particular process",
        operation_id="getProcessDescription",
    )
    def get_process_description(
        request: fastapi.Request,
        process_id: str,
    ) -> models.ProcessDescription:
        """The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process_description = client.get_process_description(process_id=process_id)
        process_description.links = [
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process_description.id}"
                ),
                rel="self",
                type="application/json",
                title="process description",
            )
        ]

        return process_description


def create_post_process_execute_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `POST /processes/{process_id}/execute`
    endpoint as implemented by `client`.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `POST /processes/{process_id}/execute` endpoint.
    """

    @router.post(
        "/{process_id}/execute",
        status_code=201,
        response_model=models.StatusInfo,
        response_model_exclude_none=True,
        response_model_exclude_unset=True,
        summary="execute a process",
        operation_id="postProcessExecution",
    )
    def post_process_execute(
        process_id: str, request_content: models.Execute, response: fastapi.Response
    ) -> Any:
        """Create a new job."""
        status_info = client.post_process_execute(
            process_id=process_id, execution_content=request_content
        )
        response.headers["Location"] = f"/jobs/{status_info.jobID}"

        return status_info


def create_get_job_status_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /jobs/{job_id}` endpoint
    as implemented by `client`.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs/{job_id}` endpoint.
    """

    @router.get(
        "/{job_id}",
        response_model=models.StatusInfo,
        response_model_exclude_none=True,
        response_model_exclude_unset=True,
        summary="retrieve status information of a job",
        operation_id="getJobStatus",
    )
    def get_job_status(
        job_id: str,
    ) -> models.StatusInfo:
        """Shows the status of a job."""
        job_status = client.get_job_status(job_id=job_id)

        return job_status


def create_get_job_results_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /jobs/{job_id}/results`
    endpoint as implemented by `client`.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs/{job_id}/results` endpoint.
    """

    @router.get(
        "/{job_id}/results",
        status_code=204,
        operation_id="getJobResults",
    )
    def get_job_results(job_id: str, response: fastapi.Response) -> dict[Any, Any]:
        """Shows results of a job."""
        results_link = client.get_job_results(job_id=job_id)
        response.headers["Link"] = results_link.json(exclude_unset=True)
        return {}


def create_processes_router(client: clients.BaseClient) -> fastapi.APIRouter:
    """Register the API router collecting the `/processes/...` endpoints.


    Parameters
    ----------
    client : clients.BaseClient
        Client implementing the API endpoints.

    Returns
    -------
    fastapi.APIRouter
        Router collecting the `/processes/...` API endpoints.
    """
    router = fastapi.APIRouter(
        prefix="/processes",
        tags=["Processes"],
    )
    create_get_processes_endpoint(router=router, client=client)
    create_get_process_description_endpoint(router=router, client=client)
    create_post_process_execute_endpoint(router=router, client=client)

    return router


def create_jobs_router(client: clients.BaseClient) -> fastapi.APIRouter:
    """Register the API router collecting the `/jobs/...` endpoints.


    Parameters
    ----------
    client : clients.BaseClient
        Client implementing the API endpoints.

    Returns
    -------
    fastapi.APIRouter
        Router collecting the `/jobs/...` API endpoints.
    """
    router = fastapi.APIRouter(
        prefix="/jobs",
        tags=["Jobs"],
    )
    create_get_job_status_endpoint(router=router, client=client)
    create_get_job_results_endpoint(router=router, client=client)

    return router
