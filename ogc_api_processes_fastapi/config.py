from typing import Dict, List, Optional

from pydantic import BaseModel


class RouteConfig(BaseModel):
    path: str
    methods: List[str]
    status_code: int = 200
    client_method: Optional[str] = None
    deprecated: Optional[bool] = None


ROUTES: Dict[str, RouteConfig] = {
    "GetLandingPage": RouteConfig(
        path="/",
        methods=["GET"],
    ),
    "GetConformance": RouteConfig(
        path="/conformance",
        methods=["GET"],
    ),
    "GetProcesses": RouteConfig(
        path="/processes",
        methods=["GET"],
        client_method="get_processes",
    ),
    "GetProcess": RouteConfig(
        path="/processes/{process_id}",
        methods=["GET"],
        client_method="get_process",
    ),
    "PostProcessExecute": RouteConfig(
        path="/processes/{process_id}/execute",
        methods=["POST"],
        status_code=201,
        client_method="post_process_execution",
        deprecated=True,
    ),
    "PostProcessExecution": RouteConfig(
        path="/processes/{process_id}/execution",
        methods=["POST"],
        status_code=201,
        client_method="post_process_execution",
    ),
    "GetJobs": RouteConfig(
        path="/jobs",
        methods=["GET"],
        client_method="get_jobs",
    ),
    "GetJob": RouteConfig(
        path="/jobs/{job_id}",
        methods=["GET"],
        client_method="get_job",
    ),
    "GetJobResults": RouteConfig(
        path="/jobs/{job_id}/results",
        methods=["GET"],
        client_method="get_job_results",
    ),
}
