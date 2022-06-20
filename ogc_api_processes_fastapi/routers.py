from typing import Any

from fastapi import APIRouter, Query, Request

from . import api
from .models import ProcessesList

processes_router = APIRouter(
    prefix="/processes",
    tags=["Processes"],
)


@processes_router.get(
    "/",
    response_model=ProcessesList,
    response_model_exclude_none=True,
    summary="retrieve the list of available processes",
    operation_id="geProcesses",
)
def get_processes_list(
    request: Request, limit: int = Query(default=10, ge=1, le=100)
) -> dict[str, list[dict[str, Any]]]:
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
