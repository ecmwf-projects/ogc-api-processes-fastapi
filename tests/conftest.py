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

from typing import Any, Dict, Iterator, List, Optional, TypedDict

import fastapi
import pytest

from ogc_api_processes_fastapi import clients, models


class Process(TypedDict):
    id: str
    version: str
    inputs: Dict[str, models.InputDescription]
    outputs: Dict[str, models.OutputDescription]


PROCESSES_DB = [
    Process(
        id=f"dataset-{i}",
        version=f"{i}.0",
        inputs={f"input-{i}": models.InputDescription(schema={"type": "string"})},
        outputs={f"output-{i}": models.OutputDescription(schema={"type": "object"})},
    )
    for i in range(10)
]


class TestClientDefault(clients.BaseClient):
    """Test implementation of the OGC API - Processes endpoints."""

    def get_processes(
        self, limit: Optional[int] = fastapi.Query(None)
    ) -> models.ProcessList:
        if not limit:
            limit = len(PROCESSES_DB)
        processes = [
            models.ProcessSummary(
                id=PROCESSES_DB[i]["id"],
                version=PROCESSES_DB[i]["version"],
            )
            for i in range(0, limit)
        ]
        process_list = models.ProcessList(
            processes=processes, links=[models.Link(href="https://example.org")]
        )
        return process_list

    def get_process(
        self, process_id: str = fastapi.Path(...)
    ) -> models.ProcessDescription:
        for i, elem in enumerate(PROCESSES_DB):
            if elem["id"] == process_id:
                process = models.ProcessDescription(
                    id=PROCESSES_DB[i]["id"],
                    version=PROCESSES_DB[i]["version"],
                    inputs=PROCESSES_DB[i]["inputs"],
                    outputs=PROCESSES_DB[i]["outputs"],
                )

        return process

    def post_process_execution(
        self,
        process_id: str = fastapi.Path(...),
        execution_content: Dict[str, Any] = fastapi.Body(...),
    ) -> models.StatusInfo:
        status_info = models.StatusInfo(
            jobID="1", status=models.StatusCode.accepted, type=models.JobType.process
        )
        return status_info

    def get_jobs(
        self,
        processID: Optional[List[str]] = fastapi.Query(None),
        status: Optional[List[str]] = fastapi.Query(None),
        limit: Optional[int] = fastapi.Query(10, ge=1, le=10000),
    ) -> models.JobList:
        jobs = [
            models.StatusInfo(
                jobID="1",
                status=models.StatusCode.accepted,
                type=models.JobType.process,
            )
        ]
        job_list = models.JobList(jobs=jobs)
        return job_list

    def get_job(self, job_id: str = fastapi.Path(...)) -> models.StatusInfo:
        status_info = models.StatusInfo(
            jobID="1", status=models.StatusCode.running, type=models.JobType.process
        )
        return status_info

    def get_job_results(
        self,
        job_id: str = fastapi.Path(...),
    ) -> models.Results:
        results = {
            "result": f"https://example.org/{job_id}-results.nc",
        }
        return results  # type: ignore

    def delete_job(self, job_id: str = fastapi.Path(...)) -> models.StatusInfo:
        status_info = models.StatusInfo(
            jobID="1", status=models.StatusCode.dismissed, type=models.JobType.process
        )
        return status_info


class StatusInfo(models.StatusInfo):
    metadata: str


class JobList(models.JobList):
    jobs: List[StatusInfo]  # type: ignore


class TestClientExtended(clients.BaseClient):
    """Test implementation of the OGC API - Processes endpoints."""

    def get_processes(
        self, limit: Optional[int] = fastapi.Query(None)
    ) -> models.ProcessList:
        if not limit:
            limit = len(PROCESSES_DB)
        processes = [
            models.ProcessSummary(
                id=PROCESSES_DB[i]["id"],
                version=PROCESSES_DB[i]["version"],
            )
            for i in range(0, limit)
        ]
        process_list = models.ProcessList(
            processes=processes, links=[models.Link(href="https://example.org")]
        )
        return process_list

    def get_process(
        self, process_id: str = fastapi.Path(...)
    ) -> models.ProcessDescription:
        for i, elem in enumerate(PROCESSES_DB):
            if elem["id"] == process_id:
                process = models.ProcessDescription(
                    id=PROCESSES_DB[i]["id"],
                    version=PROCESSES_DB[i]["version"],
                    inputs=PROCESSES_DB[i]["inputs"],
                    outputs=PROCESSES_DB[i]["outputs"],
                )

        return process

    def post_process_execution(
        self,
        process_id: str = fastapi.Path(...),
        execution_content: Dict[str, Any] = fastapi.Body(...),
    ) -> models.StatusInfo:
        status_info = models.StatusInfo(
            jobID="1", status=models.StatusCode.accepted, type=models.JobType.process
        )
        return status_info

    def get_jobs(
        self,
        processID: Optional[List[str]] = fastapi.Query(None),
        status: Optional[List[str]] = fastapi.Query(None),
        limit: Optional[int] = fastapi.Query(10, ge=1, le=10000),
    ) -> JobList:
        jobs = [
            StatusInfo(
                jobID="1",
                status=models.StatusCode.accepted,
                type=models.JobType.process,
                metadata="metadata",
            )
        ]
        job_list = JobList(jobs=jobs)
        return job_list

    def get_job(self, job_id: str = fastapi.Path(...)) -> StatusInfo:
        status_info = StatusInfo(
            jobID="1",
            status=models.StatusCode.running,
            type=models.JobType.process,
            metadata="metadata",
        )
        return status_info

    def get_job_results(  # type: ignore
        self,
        job_id: str = fastapi.Path(...),
    ) -> models.Results:
        results = {
            "result": f"https://example.org/{job_id}-results.nc",
        }
        return results  # type: ignore

    def delete_job(self, job_id: str = fastapi.Path(...)) -> StatusInfo:
        status_info = StatusInfo(
            jobID="1",
            status=models.StatusCode.dismissed,
            type=models.JobType.process,
            metadata="metadata",
        )
        return status_info


@pytest.fixture
def test_client_default() -> Iterator[clients.BaseClient]:
    yield TestClientDefault()


@pytest.fixture
def test_client_extended() -> Iterator[clients.BaseClient]:
    yield TestClientExtended()
