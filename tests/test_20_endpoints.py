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

import json
import urllib.parse

import fastapi
import fastapi.testclient

import ogc_api_processes_fastapi

BASE_URL = "http://testserver/processes/"


def test_get_processes(test_client: ogc_api_processes_fastapi.BaseClient) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    client = fastapi.testclient.TestClient(app)

    exp_processes_all = [
        {
            "id": f"retrieve-dataset-{i}",
            "version": f"{i}.0",
            "links": [
                {
                    "href": urllib.parse.urljoin(BASE_URL, f"retrieve-dataset-{i}"),
                    "rel": "self",
                    "title": "process description",
                    "type": "application/json",
                }
            ],
        }
        for i in range(10)
    ]

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


def test_get_process(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/processes/retrieve-dataset-1")
    assert response.status_code == 200

    exp_keys = ("id", "version", "inputs", "outputs")
    assert all([key in response.json() for key in exp_keys])


def test_post_process_execute(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    client = fastapi.testclient.TestClient(app)

    response = client.post("/processes/retrieve-dataset-1/execute", json={})
    assert response.status_code == 201

    exp_keys = ("jobID", "status", "type")
    assert all([key in response.json() for key in exp_keys])

    exp_headers_key = "Location"
    exp_headers_value = "/jobs/1"
    assert exp_headers_key in response.headers
    assert response.headers[exp_headers_key] == exp_headers_value


def test_get_jobs(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/jobs")
    assert response.status_code == 200

    exp_keys = ("jobs", "links")
    assert all([key in response.json() for key in exp_keys])


def test_get_job(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/jobs/job-1")
    assert response.status_code == 200

    exp_keys = ("jobID", "status", "type")
    assert all([key in response.json() for key in exp_keys])


def test_get_job_results(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/jobs/job-1/results")
    assert response.status_code == 204

    exp_headers_key = "Link"
    exp_headers_value = {
        "href": "https://example.org/job-1-results.nc",
        "title": "Download link for the result of job job-1",
    }
    assert exp_headers_key in response.headers
    assert response.headers[exp_headers_key] == json.dumps(exp_headers_value)
