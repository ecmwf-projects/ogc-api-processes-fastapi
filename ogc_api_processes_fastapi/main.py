"""API routes registration and initialization."""

import typing
from typing import Callable

import fastapi
import pydantic

from . import clients, config, endpoints, exceptions, models


def set_response_model(
    client: clients.BaseClient, route_name: str
) -> pydantic.BaseModel:
    if route_name == "GetLandingPage":
        base_model = models.LandingPage
    elif route_name == "GetConformance":
        base_model = models.ConfClass  # type: ignore
    else:
        base_model = typing.get_type_hints(
            getattr(client, config.ROUTES[route_name].client_method)  # type: ignore
        )["return"]
    response_model = pydantic.create_model(
        route_name,
        __base__=base_model,
    )

    return response_model  # type: ignore


def register_route(
    client: clients.BaseClient, router: fastapi.APIRouter, route_name: str
) -> None:
    response_model = set_response_model(client, route_name)
    route_endpoint = endpoints.create_endpoint(route_name, client=client)
    router.add_api_route(
        name=route_name,
        description=client.endpoints_description.get(route_name, ""),
        response_model=response_model,
        response_model_exclude_unset=True,
        response_model_exclude_none=True,
        endpoint=route_endpoint,
        **config.ROUTES[route_name].model_dump(exclude={"client_method"}),
    )


def register_core_routes(router: fastapi.APIRouter, client: clients.BaseClient) -> None:
    for route_name in config.ROUTES.keys():
        register_route(client, router, route_name)


def instantiate_router(client: clients.BaseClient) -> fastapi.APIRouter:
    router = fastapi.APIRouter()
    register_core_routes(router, client)
    return router


def instantiate_app(
    client: clients.BaseClient,
    exception_handler: Callable[
        [fastapi.Request, exceptions.OGCAPIException], fastapi.responses.JSONResponse
    ] = exceptions.ogc_api_exception_handler,
) -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    router = instantiate_router(client)
    app.include_router(router)
    app = exceptions.include_exception_handlers(app, exception_handler)
    return app
