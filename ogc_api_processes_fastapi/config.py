from typing import Dict, List, Optional, Union

ROUTES: Dict[str, Dict[str, Optional[Union[str, int, List[str]]]]] = {
    "GetLandingPage": {
        "path": "/",
        "methods": ["GET"],
        "client_method": None,
    },
    "GetConformance": {
        "path": "/conformance",
        "methods": ["GET"],
        "client_method": None,
    },
    "GetProcesses": {
        "path": "/processes",
        "methods": ["GET"],
        "client_method": "get_processes",
    },
    "GetProcess": {
        "path": "/processes/{process_id}",
        "methods": ["GET"],
        "client_method": "get_process",
    },
    "PostProcessExecute": {
        "path": "/processes/{process_id}/execute",
        "methods": ["POST"],
        "status_code": 201,
        "client_method": "post_process_execute",
    },
    "GetJobs": {
        "path": "/jobs",
        "methods": ["GET"],
        "client_method": "get_jobs",
    },
    "GetJob": {
        "path": "/jobs/{job_id}",
        "methods": ["GET"],
        "client_method": "get_job",
    },
    "GetJobResults": {
        "path": "/jobs/{job_id}/results",
        "methods": ["GET"],
        "client_method": "get_job_results",
    },
}
"""
    "PostProcessExecution": {
        "path": "//processes/{process_id}/execution",
        "methods": ["POST"],
    },
}
"""
