import urllib.parse
from typing import Any

import fastapi

PROCESS_LIST: list[dict[str, str]] = [
    {"id": "retrieve-reanalysis-era5-single-levels", "version": "0.1"},
    {"id": "retrieve-reanalysis-era5-pressure-levels", "version": "0.1"},
    {"id": "retrieve-reanalysis-era5-land", "version": "0.1"},
    {"id": "retrieve-reanalysis-era5-land-monthly-means", "version": "0.1"},
]


def get_processes_links(request: fastapi.Request) -> list[dict[str, Any]]:
    """
    Return links associated to the processes list request.
    """
    retval = [
        {
            "href": urllib.parse.urljoin(str(request.base_url), "processes"),
            "rel": "self",
        }
    ]
    return retval


def get_processes_list(
    limit: int = fastapi.Query(default=10, ge=1, le=100)
) -> list[dict[str, Any]]:
    """
    Return the list of processes.
    """
    return PROCESS_LIST[:limit]
