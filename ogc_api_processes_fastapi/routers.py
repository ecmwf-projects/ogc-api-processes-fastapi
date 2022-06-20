from typing import Any, Dict, List

from fastapi import APIRouter, Query

from .models import ProcessList

PROCESS_LIST: Dict[str, List[Dict[str, Any]]] = {
    "processes": [
        {"id": "retrieve-era5-single-levels", "version": "0.1"},
        {"id": "retrieve-era5-pressure-levels", "version": "0.1"},
        {"id": "retrieve-era5-land", "version": "0.1"},
        {"id": "retrieve-era5-monthly-means", "version": "0.1"},
    ],
    "links": [
        {
            "href": "http://127.0.0.1:8000/processes/",
            "rel": "self",
        }
    ],
}

processes_router = APIRouter(
    prefix="/processes",
    tags=["processes"],
)


@processes_router.get("/", response_model=ProcessList, response_model_exclude_none=True)
def get_process_list(
    limit: int = Query(default=3, ge=1, le=100)
) -> Dict[str, List[Dict[str, Any]]]:

    process_list = {
        "processes": PROCESS_LIST["processes"][0:limit],
        "links": PROCESS_LIST["links"],
    }
    return process_list
