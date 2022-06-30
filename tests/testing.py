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

from ogc_api_processes_fastapi import clients, models

PROCESSES_LIST = [
    {"id": f"retrieve-dataset-{i}", "version": f"{i}.0"} for i in range(10)
]


@attrs.define
class TestClient(clients.BaseClient):
    """
    Test implementation of the OGC API - Processes endpoints.
    """

    def get_processes_list(
        self, limit: int, offset: int
    ) -> list[models.ProcessSummary]:
        processes_list = [
            models.ProcessSummary(
                id=PROCESSES_LIST[i]["id"], version=PROCESSES_LIST[i]["version"]
            )
            for i in range(offset, offset + limit)
        ]
        return processes_list
