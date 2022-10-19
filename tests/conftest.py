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

from typing import Any, Dict, Iterator, List, Optional

import fastapi
import pytest

from ogc_api_processes_fastapi import clients, responses

PROCESSES_DB = [
    {
        "id": f"dataset-{i}",
        "version": f"{i}.0",
        "inputs": {f"input-{i}": {"schema": {"type": "string"}}},
        "outputs": {f"output-{i}": {"schema": {"type": "object"}}},
    }
    for i in range(10)
]


class TestClientDefault(clients.BaseClient):
    """
    Test implementation of the OGC API - Processes endpoints.
    """

    def get_processes(
        self, limit: Optional[int] = fastapi.Query(None)
    ) -> responses.ProcessList:
        if not limit:
            limit = len(PROCESSES_DB)
        processes = [
            responses.ProcessSummary(
                id=PROCESSES_DB[i]["id"],
                version=PROCESSES_DB[i]["version"],
            )
            for i in range(0, limit)
        ]
        process_list = responses.ProcessList(processes=processes)
        return process_list

    def get_process(
        self, process_id: str = fastapi.Path(...)
    ) -> responses.ProcessDescription:
        for i, elem in enumerate(PROCESSES_DB):
            if elem["id"] == process_id:
                process = responses.ProcessDescription(
                    id=PROCESSES_DB[i]["id"],
                    version=PROCESSES_DB[i]["version"],
                    inputs=PROCESSES_DB[i]["inputs"],
                    outputs=PROCESSES_DB[i]["outputs"],
                )

        return process

    def post_process_execute(
        self,
        process_id: str = fastapi.Path(...),
        execution_content: Dict[str, Any] = fastapi.Body(...),
    ) -> responses.StatusInfo:
        status_info = responses.StatusInfo(jobID=1, status="accepted", type="process")
        return status_info

    def get_jobs(self) -> responses.JobList:
        jobs = [responses.StatusInfo(jobID=1, status="accepted", type="process")]
        job_list = responses.JobList(jobs=jobs)
        return job_list

    def get_job(self, job_id: str = fastapi.Path(...)) -> responses.StatusInfo:
        status_info = responses.StatusInfo(jobID=1, status="running", type="process")
        return status_info

    def get_job_results(  # type: ignore
        self,
        job_id: str = fastapi.Path(...),
    ) -> Dict[str, Any]:
        results = {
            "result": f"https://example.org/{job_id}-results.nc",
        }
        return results


class StatusInfo(responses.StatusInfo):
    metadata: str


class JobList(responses.JobList):
    jobs: List[StatusInfo]  # type: ignore


class TestClientExtended(clients.BaseClient):
    """
    Test implementation of the OGC API - Processes endpoints.
    """

    def get_processes(
        self, limit: Optional[int] = fastapi.Query(None)
    ) -> responses.ProcessList:
        if not limit:
            limit = len(PROCESSES_DB)
        processes = [
            responses.ProcessSummary(
                id=PROCESSES_DB[i]["id"],
                version=PROCESSES_DB[i]["version"],
            )
            for i in range(0, limit)
        ]
        process_list = responses.ProcessList(processes=processes)
        return process_list

    def get_process(
        self, process_id: str = fastapi.Path(...)
    ) -> responses.ProcessDescription:
        for i, elem in enumerate(PROCESSES_DB):
            if elem["id"] == process_id:
                process = responses.ProcessDescription(
                    id=PROCESSES_DB[i]["id"],
                    version=PROCESSES_DB[i]["version"],
                    inputs=PROCESSES_DB[i]["inputs"],
                    outputs=PROCESSES_DB[i]["outputs"],
                )

        return process

    def post_process_execute(
        self,
        process_id: str = fastapi.Path(...),
        execution_content: Dict[str, Any] = fastapi.Body(...),
    ) -> responses.StatusInfo:
        status_info = responses.StatusInfo(jobID=1, status="accepted", type="process")
        return status_info

    def get_jobs(self) -> JobList:
        jobs = [StatusInfo(jobID=1, status="accepted", type="process")]
        job_list = JobList(jobs=jobs)
        return job_list

    def get_job(self, job_id: str = fastapi.Path(...)) -> StatusInfo:
        status_info = StatusInfo(jobID=1, status="running", type="process")
        return status_info

    def get_job_results(  # type: ignore
        self,
        job_id: str = fastapi.Path(...),
    ) -> Dict[str, Any]:
        results = {
            "result": f"https://example.org/{job_id}-results.nc",
        }
        return results


@pytest.fixture
def test_client_default() -> Iterator[clients.BaseClient]:
    yield TestClientDefault()


@pytest.fixture
def test_client_extended() -> Iterator[clients.BaseClient]:
    yield TestClientExtended()
