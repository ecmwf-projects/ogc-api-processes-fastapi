from typing import Dict, List, Optional

from pydantic import BaseModel


class RouteConfig(BaseModel):
    path: str
    summary: Optional[str] = None
    methods: List[str]
    status_code: int = 200
    client_method: Optional[str] = None
    deprecated: Optional[bool] = None


ROUTES: Dict[str, RouteConfig] = {
    "GetLandingPage": RouteConfig(
        path="/",
        summary="Landing page",
        methods=["GET"],
    ),
    "GetConformance": RouteConfig(
        path="/conformance",
        summary="Conformance classes",
        methods=["GET"],
    ),
    "GetProcesses": RouteConfig(
        path="/processes",
        summary="List of the available processes",
        methods=["GET"],
        client_method="get_processes",
    ),
    "GetProcess": RouteConfig(
        path="/processes/{process_id}",
        summary="Description of a process",
        methods=["GET"],
        client_method="get_process",
    ),
    "PostProcessExecute": RouteConfig(
        path="/processes/{process_id}/execute",
        summary="Execution of a process",
        methods=["POST"],
        status_code=201,
        client_method="post_process_execution",
        deprecated=True,
    ),
    "PostProcessExecution": RouteConfig(
        path="/processes/{process_id}/execution",
        summary="Execution of a process",
        methods=["POST"],
        status_code=201,
        client_method="post_process_execution",
    ),
    "GetJobs": RouteConfig(
        path="/jobs",
        summary="List of submitted jobs",
        methods=["GET"],
        client_method="get_jobs",
    ),
    "GetJob": RouteConfig(
        path="/jobs/{job_id}",
        summary="Status of a job",
        methods=["GET"],
        client_method="get_job",
    ),
    "GetJobResults": RouteConfig(
        path="/jobs/{job_id}/results",
        summary="Results of a job",
        methods=["GET"],
        client_method="get_job_results",
    ),
    "DeleteJob": RouteConfig(
        path="/jobs/{job_id}",
        summary="Cancel a job",
        methods=["DELETE"],
        client_method="delete_job",
    ),
}
