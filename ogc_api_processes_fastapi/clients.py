"""OGC API Processes base clients."""

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

import abc
from typing import Any, Dict, List, Optional

import fastapi

from . import responses


class BaseClient(abc.ABC):
    """Defines a pattern for implementing OGC API - Processes endpoints."""

    @abc.abstractmethod
    def get_processes(
        self, limit: Optional[int] = fastapi.Query(None)
    ) -> responses.ProcessList:
        """Get all available processes.

        Called with `GET /processes`.

        Parameters
        ----------
        limit : Optional[int] = fastapi.Query(None)
            Number of processes summaries to be returned.

        Returns
        -------
        responses.ProcessList
            List of available processes summaries.
        """
        ...

    @abc.abstractmethod
    def get_process(
        self, process_id: str = fastapi.Path(...)
    ) -> responses.ProcessDescription:
        """Get description of the process identified by `process_id`.

        Called with `GET /processes/{process_id}`.

        Parameters
        ----------
        process_id : str = fastapi.Path(...)
            Identifier of the process.

        Returns
        -------
        responses.schema["ProcessDescription"]
            Description of the process.

        Raises
        ------
        exceptions.NoSuchProcess
            If the process `process_id` is not found.
        """
        ...

    @abc.abstractmethod
    def post_process_execution(
        self,
        process_id: str = fastapi.Path(...),
        execution_content: Dict[str, Any] = fastapi.Body(...),
    ) -> responses.StatusInfo:
        """Post request for execution of the process identified by `process_id`.

        Called with `POST /processes/{process_id}/execution`.

        Parameters
        ----------
        process_id : str = fastapi.Path(...)
            Identifier of the process.
        execution_content : Dict[str, Any] = fastapi.Body(...)
            Request body containing details for the process execution
            (e.g. inputs values).

        Returns
        -------
        responses.StatusInfo
            Information on the status of the submitted job.

        Raises
        ------
        exceptions.NoSuchProcess
            If the process `process_id` is not found.
        """
        ...

    @abc.abstractmethod
    def get_jobs(
        self,
        processID: Optional[List[str]] = fastapi.Query(None),
        status: Optional[List[str]] = fastapi.Query(None),
        limit: Optional[int] = fastapi.Query(10, ge=1, le=10000),
    ) -> responses.JobList:
        """Get the list of submitted jobs.

        Called with `GET /jobs`.

        Parameters
        ----------
        processID: Optional[List[str]] = fastapi.Query(None)
            If the parameter is specified with the operation, only jobs that have a value for
            the processID property that matches one of the values specified for the processID
            parameter shall be included in the response.
        status: Optional[List[str]] = fastapi.Query(None)
            If the parameter is specified with the operation, only jobs that have a value for
            the status property that matches one of the specified values of the status parameter
            shall be included in the response.
        limit: Optional[int] = fastapi.Query(10, ge=1, le=10000)
            The response shall not contain more jobs than specified by the optional ``limit``
            parameter.

        Returns
        -------
        responses.JobList
            List of jobs.
        """

    @abc.abstractmethod
    def get_job(self, job_id: str = fastapi.Path(...)) -> responses.StatusInfo:
        """Get status information of the job identified by `job_id`.

        Called with `GET /jobs/{job_id}`.

        Parameters
        ----------
        job_id: str = fastapi.Path(...)
            Identifier of the job.

        Returns
        -------
        responses.StatusInfo
            Information on the status of the job.

        Raises
        ------
        exceptions.NoSuchJob
            If the job `job_id` is not found.
        """
        ...

    @abc.abstractmethod
    def get_job_results(self, job_id: str = fastapi.Path(...)) -> responses.Results:
        """Get results of the job identified by `job_id`.

        Called with `GET /jobs/{job_id}/results`.

        Parameters
        ----------
        job_id: str = fastapi.Path(...)
            Identifier of the job.

        Returns
        -------
        responses.Results
            Job results.

        Raises
        ------
        exceptions.NoSuchJob
            If the job `job_id` is not found.
        exceptions.ResultsNotReady
            If job `job_id` results are not yet ready.
        exceptions.JobResultsFailed
            If job `job_id` results preparation failed.
        """
        ...

    @abc.abstractmethod
    def delete_job(self, job_id: str = fastapi.Path(...)) -> responses.StatusInfo:
        """Cancel the job identified by `job_id`.

        Called with `DELETE /jobs/{job_id}`.

        Parameters
        ----------
        job_id: str = fastapi.Path(...)
            Identifier of the job.

        Returns
        -------
        responses.StatusInfo
            Information on the status of the job.

        Raises
        ------
        exceptions.NoSuchJob
            If the job `job_id` is not found.
        """
        ...
