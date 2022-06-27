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
                href=urllib.parse.urljoin(str(request.base_url), "processes"),
                rel="self",
            )
        ]
        process_list = client.get_processes_list(limit=limit, offset=offset)
        retval = models.ProcessesList(processes=process_list, links=links)

        return retval


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

    return processes_router
