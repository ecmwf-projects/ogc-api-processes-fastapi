"""OGC API Processes routes definition."""

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
from typing import Any, Dict, List

import fastapi

from . import clients, models


def make_links_to_job(
    job: models.StatusInfo, request: fastapi.Request
) -> List[models.Link]:
    """Create links to attach to provided the job.

    Parameters
    ----------
    job : models.StatusInfo
        Job to create links for.

    Returns
    -------
    List[models.Link]
        Links to attach to job.
    """
    rel_job_link = "self"
    title_job_link = None
    if not request.path_params:
        rel_job_link = "monitor"
        title_job_link = "job status info"
    links = [
        models.Link(
            href=urllib.parse.urljoin(str(request.base_url), f"jobs/{job.jobID}"),
            rel=rel_job_link,
            type="application/json",
            title=title_job_link,
        )
    ]
    if job.status in (models.StatusCode.successful, models.StatusCode.failed):
        links.append(
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{job.jobID}/results"
                ),
                rel="results",
            )
        )
    return links


def create_get_processes_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /processes` endpoint.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /processes` endpoint.
    """

    @router.get(
        "",
        response_model=models.ProcessesList,
        response_model_exclude_none=True,
        summary="retrieve the list of available processes",
        operation_id="getProcesses",
    )
    def get_processes(
        request: fastapi.Request,
        limit: int = fastapi.Query(default=10, ge=1, le=100),
        offset: int = fastapi.Query(default=0, ge=0),
    ) -> models.ProcessesList:
        """Get the list of available processes.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        processes = client.get_processes(limit=limit, offset=offset)
        for process in processes:
            process.links = [
                models.Link(
                    href=urllib.parse.urljoin(
                        str(request.base_url), f"processes/{process.id}"
                    ),
                    rel="process",
                    type="application/json",
                    title="process description",
                )
            ]
        links = [
            models.Link(
                href=urllib.parse.urljoin(str(request.base_url), "processes/"),
                rel="self",
                type="application/json",
            )
        ]
        processes_list = models.ProcessesList(processes=processes, links=links)

        return processes_list


def create_get_process_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /processes/{process_id}` endpoint.

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
    def get_process(
        request: fastapi.Request,
        process_id: str,
    ) -> models.ProcessDescription:
        """Get the description of a specific process.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process_description = client.get_process(process_id=process_id)
        process_description.links = [
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process_description.id}"
                ),
                rel="self",
                type="application/json",
            ),
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process_description.id}/execute"
                ),
                rel="execute",
                type="application/json",
                title="process execution",
            ),
        ]

        return process_description


def create_post_process_execute_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `POST /processes/{process_id}/execute` endpoint.

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
        request: fastapi.Request,
        process_id: str,
        request_content: models.Execute,
        response: fastapi.Response,
    ) -> Any:
        """Create a new job."""
        status_info = client.post_process_execute(
            process_id=process_id,
            execution_content=request_content,
            request=request,
            response=response,
        )
        status_info["links"] = [
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process_id}/execute"
                ),
                rel="self",
                type="application/json",
            ),
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{status_info['jobID']}"
                ),
                rel="monitor",
                type="application/json",
                title="job status info",
            ),
        ]
        response.headers["Location"] = urllib.parse.urljoin(
            str(request.base_url), f"jobs/{status_info['jobID']}"
        )

        return status_info


def create_get_jobs_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /jobs` endpoint.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs` endpoint.
    """

    @router.get(
        "",
        response_model=models.JobList,
        response_model_exclude_none=True,
        response_model_exclude_unset=True,
        summary="retrieve the list of submitted jobs",
        operation_id="getJobs",
    )
    def get_jobs(request: fastapi.Request) -> models.JobList:
        """Show the list of submitted jobs."""
        jobs_list = client.get_jobs()
        for job in jobs_list:
            job.links = make_links_to_job(job=job, request=request)
        jobs = models.JobList(
            jobs=jobs_list,
            links=[
                models.Link(
                    href=urllib.parse.urljoin(str(request.base_url), "jobs"),
                    rel="self",
                    type="application/json",
                    title="list of submitted jobs",
                )
            ],
        )

        return jobs


def create_get_job_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /jobs/{job_id}` endpoint.

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
    def get_job(
        request: fastapi.Request,
        job_id: str,
    ) -> models.StatusInfo:
        """Show the status of a job."""
        job = client.get_job(job_id=job_id)
        job.links = make_links_to_job(job=job, request=request)

        return job


def create_get_job_results_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    """Add to the provided `router` the `GET /jobs/{job_id}/results` endpoint.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs/{job_id}/results` endpoint.
    """

    @router.get(
        "/{job_id}/results",
        response_model=models.Results,
        response_model_exclude_unset=True,
        responses={
            404: {"description": "Job not found", "model": models.Exception},
        },
        operation_id="getJobResults",
    )
    def get_job_results(job_id: str) -> Dict[str, Any]:
        """Show results of a job."""
        response = client.get_job_results(job_id=job_id)

        return response


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
    create_get_process_endpoint(router=router, client=client)
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
    create_get_job_endpoint(router=router, client=client)
    create_get_jobs_endpoint(router=router, client=client)
    create_get_job_results_endpoint(router=router, client=client)

    return router
