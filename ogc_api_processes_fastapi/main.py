import fastapi

from . import clients, routers


def instantiate_ogc_api_processes_app(client: clients.BaseClient) -> fastapi.FastAPI:
    """
    Create an instance of an OGC API - Processes compliant FastAPI application.

    Arguments:
        client:
            Defines the application logic which is injected into the API.

    Returns:
        app:
            The FastAPI application.
    """
    app = fastapi.FastAPI()
    processes_router = routers.create_processes_router(client=client)
    app.include_router(processes_router)

    return app


def include_ogc_api_processes_routers(
    app: fastapi.FastAPI, client: clients.BaseClient
) -> fastapi.FastAPI:
    """
    Add OGC API - Processes compliant routers to a FastAPI application.

    Arguments:
        app:
            A FastAPI application.
        client:
            Defines the application logic which is injected into the API.

    Returns:
        app:
            A FastAPI application with OGC API - Processes routes added.
    """
    processes_router = routers.create_processes_router(client=client)
    app.include_router(processes_router)

    return app
