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
    def get_processes_list(
        self, limit: int, offset: int
    ) -> List[models.ProcessSummary]:
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
    def get_process_description(self, process_id: str) -> models.ProcessDescription:
        """Get description of process `process_id`.

        Called with `GET /processes/{process_id}`.

        Parameters
        ----------
        process_id : str
            Identifier of the process.

        Returns
        -------
        models.ProcessDescription
            Description of the process identfied by `process_id`.
        """
        ...

    @abc.abstractmethod
    def post_process_execute(
        self, process_id: str, execution_content: models.Execute
    ) -> models.StatusInfo:
        """Post request for execution of process `process_id`.

        Called with `POST /processes/{process_id}/execute`.

        Parameters
        ----------
        process_id : str
            Identifier of the process.
        execution_content : models.Execute
            Request body containing details for the process execution (e.g. inputs values)

        Returns
        -------
        Any
            Information on the status of the job.
        """
        ...
