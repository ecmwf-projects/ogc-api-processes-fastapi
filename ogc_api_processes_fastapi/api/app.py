"fastapi app creation"

import attr


@attr.define()
class ProcessingAPI:
    """
    ProcessingAPI factory.

    Factory for creating an OGC FastAPI application.  After instantation, the application is accessible from
    the `StacApi.app` attribute.
    """

    ...
