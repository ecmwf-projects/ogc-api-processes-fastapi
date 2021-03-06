"""Instantiation methods for an OGC API Processes compliant FastAPI application."""

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

import fastapi

from . import clients, exceptions, routers


def include_routers(
    app: fastapi.FastAPI, client: clients.BaseClient
) -> fastapi.FastAPI:
    """Add OGC API - Processes compliant routers to a FastAPI application.

    Parameters
    ----------
    app : fastapi.FastAPI
        FastAPI application to which OGC API - Processes compliant routers
        should be added.
    client : clients.BaseClient
        Client implementing the API endpoints.

    Returns
    -------
    fastapi.FastAPI
        FastAPI application including OGC API - Processes compliant routes.
    """
    processes_router = routers.create_processes_router(client=client)
    app.include_router(processes_router)
    jobs_router = routers.create_jobs_router(client=client)
    app.include_router(jobs_router)

    return app


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
    app.add_exception_handler(
        exceptions.NoSuchProcess, exceptions.no_such_process_exception_handler
    )
    app.add_exception_handler(
        exceptions.NoSuchJob, exceptions.no_such_job_exception_handler
    )
    app.add_exception_handler(
        exceptions.ResultsNotReady, exceptions.results_not_ready_exception_handler
    )
    app.add_exception_handler(
        exceptions.JobResultsFailed, exceptions.job_results_failed_exception_handler
    )
    return app


def instantiate_app(client: clients.BaseClient) -> fastapi.FastAPI:
    """Create an instance of an OGC API - Processes compliant FastAPI application.

    Parameters
    ----------
    client : clients.BaseClient
        Client implementing the API endpoints.

    Returns
    -------
    fastapi.FastAPI
        OGC API - Processes compliant FastAPI application.
    """
    app = fastapi.FastAPI()
    app = include_routers(app=app, client=client)

    return app
