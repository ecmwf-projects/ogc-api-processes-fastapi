from typing import Any

import fastapi

from . import clients, models


def _register_get_processes(
    router: fastapi.APIRouter, client: clients.BaseClient
) -> None:
    @router.get(
        "/",
        response_model=models.ProcessesList,
        response_model_exclude_none=True,
        summary="retrieve the list of available processes",
        operation_id="geProcesses",
    )
    def get_processes_list(
        request: fastapi.Request, limit: int = fastapi.Query(default=10, ge=1, le=100)
    ) -> dict[str, list[dict[str, Any]]]:
        """
        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process_list = client.get_processes(request=request)
        return process_list


def register_processes_router(client: clients.BaseClient) -> fastapi.APIRouter:

    processes_router = fastapi.APIRouter(
        prefix="/processes",
        tags=["Processes"],
    )

    _register_get_processes(router=processes_router, client=client)

    return processes_router
