"""API routes registration and initialization."""

from typing import Any, Dict

import attrs
import fastapi

from . import clients, endpoints, responses

ROUTES = {
    "GetLandingPage": {"path": "/", "methods": ["GET"]},
    "GetConformance": {"path": "/conformance", "methods": ["GET"]},
    "GetProcesses": {"path": "/processes", "methods": ["GET"]},
    "GetProcess": {"path": "/processes/{process_id}", "methods": ["GET"]},
    "PostProcessExecute": {
        "path": "/processes/{process_id}/execute",
        "methods": ["POST"],
        "status_code": 201,
    },
    "GetJobs": {"path": "/jobs", "methods": ["GET"]},
    "GetJob": {"path": "/jobs/{job_id}", "methods": ["GET"]},
    "GetJobResults": {"path": "/jobs/{job_id}/results", "methods": ["GET"]},
}
"""
    "PostProcessExecution": {
        "path": "//processes/{process_id}/execution",
        "methods": ["POST"],
    },
}
"""


@attrs.define
class OGCProcessesAPI:

    client: clients.BaseClient
    router: fastapi.APIRouter = attrs.field(default=attrs.Factory(fastapi.APIRouter))
    app: fastapi.FastAPI = attrs.field(default=attrs.Factory(fastapi.FastAPI))
    add_resp_params: Dict[str, Any] = attrs.field(default={"Posts": {}})

    def register_route(self, route_name, schema):
        route_endpoint = endpoints.create_endpoint(
            route_name, client=self.client, schema=schema
        )
        self.router.add_api_route(
            name=route_name,
            path=ROUTES[route_name]["path"],
            response_model=schema,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            status_code=ROUTES[route_name].get("status_code", 200),
            methods=ROUTES[route_name]["methods"],
            endpoint=route_endpoint,
        )

    def register_core(self, schema):
        for route_name in ROUTES.keys():
            self.register_route(route_name, schema[route_name])

    def __attrs_post_init__(self):
        schema = responses.generate_schema(self.add_resp_params)
        self.register_core(schema)
        self.app.include_router(self.router)
