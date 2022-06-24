import abc
from typing import Any

import fastapi

from . import models


class BaseClient(abc.ABC):
    """
    Defines a pattern for implementing OGC API - Processes endpoints.
    """

    @abc.abstractmethod
    def get_processes(self, **kwargs: Any) -> dict[str, list[dict[str, Any]]]:
        """
        Get all available processes.

        Called with `GET /processes`.

        Returns:
            An object of type models.ProcessesList.
        """
        ...


def instantiate_app(client: BaseClient) -> fastapi.FastAPI:
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

    processes_router = fastapi.APIRouter(
        prefix="/processes",
        tags=["Processes"],
    )

    @processes_router.get(
        "/",
        response_model=models.ProcessesList,
        response_model_exclude_none=True,
        summary="retrieve the list of available processes",
        operation_id="geProcesses",
    )
    def get_processes_list(
        request: fastapi.Request, limit: int = fastapi.Query(default=10, ge=1, le=100)
    ) -> dict[str, list[dict[str, Any]]]:
        """
        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process_list = client.get_processes(request=request)
        return process_list

    app.include_router(processes_router)

    return app
