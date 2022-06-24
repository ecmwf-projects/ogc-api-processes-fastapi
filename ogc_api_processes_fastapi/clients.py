import abc
from typing import Any


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
