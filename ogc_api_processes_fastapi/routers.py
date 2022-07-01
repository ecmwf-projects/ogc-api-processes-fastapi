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

import fastapi

from . import clients, models


def _create_get_processes_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
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
        """
        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        links = [
            models.Link(
                href=urllib.parse.urljoin(str(request.base_url), "processes/"),
                rel="self",
            )
        ]
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
        retval = models.ProcessesList(processes=process_list, links=links)

        return retval


def _create_get_process_description_endpoint(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    @router.get(
        "/{processID}",
        response_model=models.Process,
        response_model_exclude_none=True,
        summary="retrieve the description of a particular process",
        operation_id="getProcessDescription",
    )
    def get_process_description(
        request: fastapi.Request,
        processID: str,
    ) -> models.Process:
        """
        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process_description = client.get_process_description(process_id=processID)
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


def create_processes_router(client: clients.BaseClient) -> fastapi.APIRouter:
    """
    Register the API router dedicated to the `/processes/...` endpoints.

    Arguments:
        client:
            Defines the application logic which is injected into the API.

    Return:
        processes_router:
            Registered router.
    """
    processes_router = fastapi.APIRouter(
        prefix="/processes",
        tags=["Processes"],
    )
    _create_get_processes_endpoint(router=processes_router, client=client)
    _create_get_process_description_endpoint(router=processes_router, client=client)

    return processes_router
