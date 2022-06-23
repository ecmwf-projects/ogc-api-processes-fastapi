import abc
import typing as T

from . import models


class BaseClient(abc.ABC):
    """
    Defines a pattern for implementing OGC API - Processes endpoints.
    """

    @abc.abstractmethod
    def get_processes(self, **kwargs: T.Any) -> models.ProcessesList:
        """
        Get all available processes.

        Called with `GET /processes`.

        Returns:
            An object of type models.ProcessesList.
        """
        ...
