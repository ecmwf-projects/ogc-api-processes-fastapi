"""OGC API Processes exceptions and exceptions handling."""

# Copyright 2022, European Union.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

from typing import Optional

import attrs
import fastapi

from . import models


@attrs.define
class OGCAPIException(Exception):
    type: str
    status_code: int
    title: Optional[str] = None
    detail: Optional[str] = None
    instance: Optional[str] = None


@attrs.define
class NoSuchProcess(OGCAPIException):
    type: str = (
        "http://www.opengis.net/def/exceptions/ogcapi-processes-1/1.0/no-such-process"
    )
    status_code: int = fastapi.status.HTTP_404_NOT_FOUND


@attrs.define
class NoSuchJob(OGCAPIException):
    type: str = (
        "http://www.opengis.net/def/exceptions/ogcapi-processes-1/1.0/no-such-job"
    )
    status_code: int = fastapi.status.HTTP_404_NOT_FOUND


@attrs.define
class ResultsNotReady(OGCAPIException):
    type: str = (
        "http://www.opengis.net/def/exceptions/ogcapi-processes-1/1.0/result-not-ready"
    )
    status_code: int = fastapi.status.HTTP_404_NOT_FOUND


@attrs.define
class JobResultsFailed(OGCAPIException):
    type: str = "generic error"
    status_code: int = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR


def ogc_api_exception_handler(
    request: fastapi.Request, exc: OGCAPIException
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=exc.status_code,
        content=models.Exception(
            type=exc.type,
            title=exc.title,
            status=exc.status_code,
            detail=exc.detail,
            instance=str(request.url),
        ).dict(exclude_none=True),
    )


def include_exception_handlers(app: fastapi.FastAPI) -> fastapi.FastAPI:
    """Add OGC API - Processes compliatn exceptions handlers to a FastAPI application.

    Parameters
    ----------
    app : fastapi.FastAPI
        FastAPI application to which OGC API - Processes compliant exceptions handlers.
        should be added.

    Returns
    -------
    fastapi.FastAPI
        FastAPI application including OGC API - Processes compliant exceptions handlers.
    """
    app.add_exception_handler(NoSuchProcess, ogc_api_exception_handler)
    app.add_exception_handler(NoSuchJob, ogc_api_exception_handler)
    app.add_exception_handler(ResultsNotReady, ogc_api_exception_handler)
    app.add_exception_handler(JobResultsFailed, ogc_api_exception_handler)
    return app
