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
from typing import List

from . import models


class BaseClient(abc.ABC):
    """Defines a pattern for implementing OGC API - Processes endpoints."""

    @abc.abstractmethod
    def get_processes(self, limit: int, offset: int) -> List[models.ProcessSummary]:
        """Get all available processes.

        Called with `GET /processes`.

        Parameters
        ----------
        limit : int
            Number of processes summaries to be returned.
        offset : int
            Index (starting from 0) of the first process summary to be returned.

        Returns
        -------
        List[models.ProcessSummary]
            List of available processes summaries.
        """
        ...

    @abc.abstractmethod
    def get_process(self, process_id: str) -> models.ProcessDescription:
        """Get description of the process identified by `process_id`.

        Called with `GET /processes/{process_id}`.

        Parameters
        ----------
        process_id : str
            Identifier of the process.

        Returns
        -------
        models.ProcessDescription
            Description of the process.
        """
        ...

    @abc.abstractmethod
    def post_process_execute(
        self, process_id: str, execution_content: models.Execute
    ) -> models.StatusInfo:
        """Post request for execution of the process identified by `process_id`.

        Called with `POST /processes/{process_id}/execute`.

        Parameters
        ----------
        process_id : str
            Identifier of the process.
        execution_content : models.Execute
            Request body containing details for the process execution
            (e.g. inputs values)

        Returns
        -------
        models.StatusInfo
            Information on the status of the submitted job.
        """
        ...

    @abc.abstractmethod
    def get_jobs(self) -> List[models.StatusInfo]:
        """Get the list of submitted jobs.

        Called with `GET /jobs`.

        Parameters
        ----------
        ...

        Returns
        -------
        models.JobsList
            List of jobs.
        """

    @abc.abstractmethod
    def get_job(self, job_id: str) -> models.StatusInfo:
        """Get status information of the job identified by `job_id`.

        Called with `GET /jobs/{job_id}`.

        Parameters
        ----------
        job_id : str
            Identifier of the job.

        Returns
        -------
        models.StatusInfo
            Information on the status of the job.
        """
        ...

    # NOTE: this is tailored for the specific CADS implementation.
    @abc.abstractmethod
    def get_job_results(self, job_id: str) -> models.Link:
        """Get results of the job identified by `job_id`.

        Called with `GET /jobs/{job_id}/results`.

        Parameters
        ----------
        job_id : str
            Identifier of the job.

        Returns
        -------
        models.Link
            Link to download the job results.
        """
        ...
