import urllib.parse
from typing import Any, Dict, List

from fastapi import Request


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
