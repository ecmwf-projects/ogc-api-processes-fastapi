import typing as T

import fastapi

from . import api, models

processes_router = fastapi.APIRouter(
    prefix="/processes",
    tags=["Processes"],
)


@processes_router.get(
    "/",
    response_model=models.ProcessesList,
    response_model_exclude_none=True,
    summary="retrieve the list of available processes",
    operation_id="geProcesses",
)
def get_processes_list(
    request: fastapi.Request, limit: int = fastapi.Query(default=10, ge=1, le=100)
) -> dict[str, list[dict[str, T.Any]]]:
    """
    The list of processes contains a summary of each process
    the OGC API - Processes offers, including the link to a
    more detailed description of the process.
    """
    process_list = {
        "processes": api.get_processes_list(limit=limit),
        "links": api.get_processes_links(request),
    }
    return process_list
