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

import urllib.parse

import fastapi
import fastapi.testclient

import ogc_api_processes_fastapi

BASE_URL = "http://testserver/processes/"


def test_get_processes(test_client: ogc_api_processes_fastapi.BaseClient) -> None:
    app = ogc_api_processes_fastapi.instantiate_ogc_api_processes_app(
        client=test_client
    )
    client = fastapi.testclient.TestClient(app)

    exp_processes_all = test_client.PROCESSES_LIST.copy()
    for elem in exp_processes_all:
        elem.update(
            {
                "links": [
                    {
                        "href": urllib.parse.urljoin(BASE_URL, elem["id"]),
                        "rel": "self",
                        "title": "process description",
                        "type": "application/json",
                    }
                ]
            }
        )

    response = client.get("/processes")
    assert response.status_code == 200

    exp_keys = ("processes", "links")
    assert all([key in response.json() for key in exp_keys])

    assert response.json()["processes"] == exp_processes_all

    exp_links = [{"href": BASE_URL, "rel": "self"}]
    assert response.json()["links"] == exp_links

    offset = 5
    limit = 2
    response = client.get(f"/processes?offset={offset}&limit={limit}")
    assert response.status_code == 200

    exp_processes = exp_processes_all[slice(offset, offset + limit)]
    assert response.json()["processes"] == exp_processes
