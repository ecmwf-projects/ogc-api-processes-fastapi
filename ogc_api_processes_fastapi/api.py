"""API routes registration and initialization."""

import typing

import attrs
import fastapi

from . import clients, config, endpoints, responses


@attrs.define
class OGCProcessesAPI:

    client: clients.BaseClient
    router: fastapi.APIRouter = attrs.field(default=attrs.Factory(fastapi.APIRouter))
    app: fastapi.FastAPI = attrs.field(default=attrs.Factory(fastapi.FastAPI))

    def register_route(self, route_name):
        if route_name == "GetLandingPage":
            response_model = responses.LandingPage
        elif route_name == "GetConformance":
            response_model = responses.ConfClass
        else:
            response_model = typing.get_type_hints(
                getattr(self.client, config.ROUTES[route_name]["client_method"])
            )["return"]
        route_endpoint = endpoints.create_endpoint(route_name, client=self.client)
        self.router.add_api_route(
            name=route_name,
            path=config.ROUTES[route_name]["path"],
            response_model=response_model,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            status_code=config.ROUTES[route_name].get("status_code", 200),
            methods=config.ROUTES[route_name]["methods"],
            endpoint=route_endpoint,
        )

    def register_core(self):
        for route_name in config.ROUTES.keys():
            self.register_route(route_name)

    def __attrs_post_init__(self):
        self.register_core()
        self.app.include_router(self.router)
