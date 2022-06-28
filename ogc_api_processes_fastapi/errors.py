class OGCProcessesApiError(Exception):
    """Generic API error."""

    pass


class ConflictError(OGCProcessesApiError):
    """Database conflict."""

    pass


class NotFoundError(OGCProcessesApiError):
    """Resource not found."""

    pass


class ForeignKeyError(OGCProcessesApiError):
    """Foreign key error (process does not exist)."""

    pass


class DatabaseError(OGCProcessesApiError):
    """Generic database errors."""

    pass


class InvalidQueryParameter(OGCProcessesApiError):
    """Error for unknown or invalid query parameters.
    Used to capture errors that should respond according to
    http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#query_parameters
    """

    pass
