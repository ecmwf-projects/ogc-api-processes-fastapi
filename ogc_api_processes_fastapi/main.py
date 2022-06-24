import fastapi

from . import clients, routers


def instantiate_app(client: clients.BaseClient) -> fastapi.FastAPI:
    """
    Create an in instance of an OGC API - Processing compliant FastAPI application.

    Arguments:
        client:
            A subclass of `BaseClient`. Defines the application logic which is injected into the API.

    Returns:
        app:
            The FastAPI application.
    """

    app = fastapi.FastAPI()

    processes_router = routers.register_processes_router(client=client)

    app.include_router(processes_router)

    return app
