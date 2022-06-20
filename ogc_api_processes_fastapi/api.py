import urllib.parse
from typing import Any, Dict, List

from fastapi import Query, Request

PROCESS_LIST: List[Dict[str, str]] = [
    {"id": "retrieve-era5-single-levels", "version": "0.1"},
    {"id": "retrieve-era5-pressure-levels", "version": "0.1"},
    {"id": "retrieve-era5-land", "version": "0.1"},
    {"id": "retrieve-era5-monthly-means", "version": "0.1"},
]


def get_processes_links(request: Request) -> List[Dict[str, Any]]:
    """
    Return links associated to the processes list request.
    """
    return [
        {
            "href": urllib.parse.urljoin(str(request.base_url), "processes"),
            "rel": "self",
        }
    ]


def get_processes_list(
    limit: int = Query(default=10, ge=1, le=100)
) -> List[Dict[str, Any]]:
    """
    Return the list of processes.
    """
    return PROCESS_LIST[:limit]
