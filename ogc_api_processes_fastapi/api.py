"""API routes registration and initialization."""

from typing import Any, Dict

import attrs
import fastapi

from . import clients, config, endpoints, responses


@attrs.define
class OGCProcessesAPI:

    client: clients.BaseClient
    router: fastapi.APIRouter = attrs.field(default=attrs.Factory(fastapi.APIRouter))
    app: fastapi.FastAPI = attrs.field(default=attrs.Factory(fastapi.FastAPI))
    add_resp_params: Dict[str, Any] = attrs.field(default={"Posts": {}})

    def register_route(self, route_name, schema):
        route_endpoint = endpoints.create_endpoint(route_name, client=self.client)
        self.router.add_api_route(
            name=route_name,
            path=config.ROUTES[route_name]["path"],
            response_model=schema,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            status_code=config.ROUTES[route_name].get("status_code", 200),
            methods=config.ROUTES[route_name]["methods"],
            endpoint=route_endpoint,
        )

    def register_core(self, schema):
        for route_name in config.ROUTES.keys():
            self.register_route(
                route_name, schema[config.ROUTES[route_name]["response_model"]]
            )

    def __attrs_post_init__(self):
        schema = responses.generate_schema(self.add_resp_params)
        self.register_core(schema)
        self.app.include_router(self.router)
