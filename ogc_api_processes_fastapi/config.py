ROUTES = {
    "GetLandingPage": {
        "path": "/",
        "methods": ["GET"],
        "response_model": "LandingPage",
    },
    "GetConformance": {
        "path": "/conformance",
        "methods": ["GET"],
        "response_model": "ConfClass",
    },
    "GetProcesses": {
        "path": "/processes",
        "methods": ["GET"],
        "response_model": "ProcessesList",
    },
    "GetProcess": {
        "path": "/processes/{process_id}",
        "methods": ["GET"],
        "response_model": "ProcessDescription",
    },
    "PostProcessExecute": {
        "path": "/processes/{process_id}/execute",
        "methods": ["POST"],
        "status_code": 201,
        "response_model": "StatusInfo",
    },
    "GetJobs": {"path": "/jobs", "methods": ["GET"], "response_model": "JobList"},
    "GetJob": {
        "path": "/jobs/{job_id}",
        "methods": ["GET"],
        "response_model": "StatusInfo",
    },
    "GetJobResults": {
        "path": "/jobs/{job_id}/results",
        "methods": ["GET"],
        "response_model": "Results",
    },
}
"""
    "PostProcessExecution": {
        "path": "//processes/{process_id}/execution",
        "methods": ["POST"],
    },
}
"""
