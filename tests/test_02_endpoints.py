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
import fastapi.testclient

from ogc_api_processes_fastapi import main

from . import testing


def test_get_processes() -> None:
    app = main.instantiate_ogc_api_processes_app(client=testing.TestClient())
    client = fastapi.testclient.TestClient(app)

    response = client.get("/processes")
    assert response.status_code == 200

    expected_keys = ("processes", "links")
    assert all([key in response.json() for key in expected_keys])

    expected_processes = testing.PROCESSES_LIST
    assert response.json()["processes"] == expected_processes

    expected_links = [{"href": "http://testserver/processes", "rel": "self"}]
    assert response.json()["links"] == expected_links

    offset = 5
    limit = 2
    response = client.get(f"/processes?offset={offset}&limit={limit}")
    assert response.status_code == 200

    expected_processes = testing.PROCESSES_LIST[slice(offset, offset + limit)]
    assert response.json()["processes"] == expected_processes
