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

import attrs
import fastapi


class NoSuchProcess(Exception):
    ...


class NoSuchJob(Exception):
    ...


class ResultsNotReady(Exception):
    ...


@attrs.define
class JobResultsFailed(Exception):

    type: str = "generic error"
    status_code: int = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    title: str = "job failed"
    detail: str = "job failed"


def no_such_process_exception_handler(
    request: fastapi.Request, exc: Exception
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content={
            "type": "http://www.opengis.net/def/exceptions/ogcapi-processes-1/1.0/no-such-process",
            "title": "process not found",
            "detail": f"process {request.path_params['process_id']} has not been found",
            "instance": str(request.url),
        },
    )


def no_such_job_exception_handler(
    request: fastapi.Request, exc: Exception
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content={
            "type": "http://www.opengis.net/def/exceptions/ogcapi-processes-1/1.0/no-such-job",
            "title": "job not found",
            "detail": f"job {request.path_params['job_id']} has not been found",
            "instance": str(request.url),
        },
    )


def results_not_ready_exception_handler(
    request: fastapi.Request, exc: Exception
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        content={
            "type": "http://www.opengis.net/def/exceptions/ogcapi-processes-1/1.0/result-not-ready",
            "title": "job results not ready",
            "detail": f"job {request.path_params['job_id']} results are not yet ready",
            "instance": str(request.url),
        },
    )


def job_results_failed_exception_handler(
    request: fastapi.Request, exc: JobResultsFailed
) -> fastapi.responses.JSONResponse:
    return fastapi.responses.JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.type,
            "title": exc.title,
            "detail": exc.detail,
            "instance": str(request.url),
        },
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
    app.add_exception_handler(NoSuchProcess, no_such_process_exception_handler)
    app.add_exception_handler(NoSuchJob, no_such_job_exception_handler)
    app.add_exception_handler(ResultsNotReady, results_not_ready_exception_handler)
    app.add_exception_handler(JobResultsFailed, job_results_failed_exception_handler)
    return app
