"""API routes registration and initialization."""

import typing

import fastapi
import pydantic

from . import clients, config, endpoints, responses


def set_response_model(
    client: clients.BaseClient, route_name: str
) -> pydantic.BaseModel:
    if route_name == "GetLandingPage":
        base_model = responses.LandingPage
    elif route_name == "GetConformance":
        base_model = responses.ConfClass  # type: ignore
    else:
        base_model = typing.get_type_hints(
            getattr(client, config.ROUTES[route_name].client_method)  # type: ignore
        )["return"]
    response_model = pydantic.create_model(
        route_name,
        __base__=base_model,
    )
    if route_name in ("GetProcesses", "GetJobs"):
        response_model.__fields__["links"].required = True

    return response_model  # type: ignore


def register_route(
    client: clients.BaseClient, router: fastapi.APIRouter, route_name: str
) -> None:
    response_model = set_response_model(client, route_name)
    route_endpoint = endpoints.create_endpoint(route_name, client=client)
    router.add_api_route(
        name=route_name,
        path=config.ROUTES[route_name].path,
        deprecated=config.ROUTES[route_name].deprecated,
        response_model=response_model,
        response_model_exclude_unset=False,
        response_model_exclude_none=True,
        status_code=config.ROUTES[route_name].status_code,
        methods=config.ROUTES[route_name].methods,
        endpoint=route_endpoint,
    )


def register_core_routes(router: fastapi.APIRouter, client: clients.BaseClient) -> None:
    for route_name in config.ROUTES.keys():
        register_route(client, router, route_name)


def instantiate_router(client: clients.BaseClient) -> fastapi.APIRouter:
    router = fastapi.APIRouter()
    register_core_routes(router, client)
    return router


def instantiate_app(client: clients.BaseClient) -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    router = instantiate_router(client)
    app.include_router(router)
    return app
