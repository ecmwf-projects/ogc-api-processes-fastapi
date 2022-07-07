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

from typing import Iterator, List

import pytest

from ogc_api_processes_fastapi import clients, models

PROCESSES_DB = [
    {
        "id": f"retrieve-dataset-{i}",
        "version": f"{i}.0",
        "inputs": [{f"input-{i}": {"schema": {"type": "string"}}}],
        "outputs": [{f"output-{i}": {"schema": {"type": "object"}}}],
    }
    for i in range(10)
]


class TestClient(clients.BaseClient):
    """
    Test implementation of the OGC API - Processes endpoints.
    """

    def get_processes_list(
        self, limit: int, offset: int
    ) -> List[models.ProcessSummary]:
        processes_list = [
            models.ProcessSummary(
                id=PROCESSES_DB[i]["id"],
                version=PROCESSES_DB[i]["version"],
            )
            for i in range(offset, offset + limit)
        ]
        return processes_list

    def get_process_description(self, process_id: str) -> models.ProcessDescription:
        for i, elem in enumerate(PROCESSES_DB):
            if elem["id"] == process_id:
                process = models.ProcessDescription(
                    id=PROCESSES_DB[i]["id"],
                    version=PROCESSES_DB[i]["version"],
                    inputs=PROCESSES_DB[i]["inputs"],
                    outputs=PROCESSES_DB[i]["outputs"],
                )

        return process

    def post_process_execute(
        self,
        process_id: str,
        execution_content: models.Execute,
    ) -> models.StatusInfo:
        status_info = models.StatusInfo(
            jobID=1, status=models.StatusCode.accepted, type=models.JobType.process
        )
        return status_info


@pytest.fixture
def test_client() -> Iterator[clients.BaseClient]:
    yield TestClient()
