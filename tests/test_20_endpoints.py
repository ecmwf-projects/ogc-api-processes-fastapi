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
import pytest

import ogc_api_processes_fastapi
from ogc_api_processes_fastapi import endpoints, responses

BASE_URL = "http://testserver/processes/"


def test_create_self_link() -> None:
    request_url = "http://localhost/myapi"
    self_link = endpoints.create_self_link(request_url)
    exp_link = responses.Link(href=request_url, rel="self")
    assert self_link == exp_link

    self_link = endpoints.create_self_link(request_url, title="Title", type="Type")
    exp_link = responses.Link(href=request_url, rel="self", title="Title", type="Type")
    assert self_link == exp_link


def test_create_page_link() -> None:
    request_url = "http://localhost/myapi"
    page = "next"
    pagination_qs = responses.PaginationQueryParameters(
        next={"cursor": "mycursor", "back": "True"}
    )
    link_page = endpoints.create_page_link(request_url, page, pagination_qs)
    exp_link = responses.Link(
        href=f"{request_url}?cursor=mycursor&back=True", rel="next"
    )
    assert link_page == exp_link

    request_url = "http://localhost/myapi"
    page = "previous"
    pagination_qs = responses.PaginationQueryParameters(
        next={"cursor": "mycursor", "back": "True"}
    )
    with pytest.raises(ValueError):
        link_page = endpoints.create_page_link(request_url, page, pagination_qs)


def test_create_pagination_links() -> None:
    request_url = "http://localhost/myapi"
    pagination_qs = responses.PaginationQueryParameters(
        prev={"cursor": "mycursor", "back": "False"}
    )
    pagination_links = endpoints.create_pagination_links(request_url, pagination_qs)
    exp_links = [
        responses.Link(href=f"{request_url}?cursor=mycursor&back=False", rel="prev")
    ]
    assert pagination_links == exp_links


def test_get_processes(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.main.instantiate_app(client=test_client_default)
    client = fastapi.testclient.TestClient(app)

    exp_processes_all = [
        {
            "id": f"dataset-{i}",
            "version": f"{i}.0",
            "links": [
                {
                    "href": urllib.parse.urljoin(BASE_URL, f"dataset-{i}"),
                    "rel": "process",
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

    exp_links = [
        {"href": BASE_URL.rstrip("/"), "rel": "self", "type": "application/json"}
    ]
    assert response.json()["links"] == exp_links

    limit = 2
    response = client.get(f"/processes?&limit={limit}")
    assert response.status_code == 200

    exp_processes = exp_processes_all[slice(0, limit)]
    assert response.json()["processes"] == exp_processes


def test_get_process(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.main.instantiate_app(client=test_client_default)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/processes/dataset-1")
    assert response.status_code == 200

    exp_keys = ("id", "version", "inputs", "outputs")
    assert all([key in response.json() for key in exp_keys])


def test_post_process_execution(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.main.instantiate_app(client=test_client_default)
    client = fastapi.testclient.TestClient(app)

    response = client.post("/processes/dataset-1/execution", json={})
    assert response.status_code == 201

    exp_keys = ("jobID", "status", "type")
    assert all([key in response.json() for key in exp_keys])

    exp_headers_key = "Location"
    exp_headers_value = "http://testserver/jobs/1"
    assert exp_headers_key in response.headers
    assert response.headers[exp_headers_key] == exp_headers_value


def test_get_jobs(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.main.instantiate_app(client=test_client_default)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/jobs")
    assert response.status_code == 200

    exp_keys = ("jobs", "links")
    assert all([key in response.json() for key in exp_keys])


def test_get_job(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.main.instantiate_app(client=test_client_default)
    client = fastapi.testclient.TestClient(app)

    response = client.get("/jobs/job-1")
    assert response.status_code == 200

    exp_keys = ("jobID", "status", "type")
    assert all([key in response.json() for key in exp_keys])


def test_get_job_results(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.main.instantiate_app(client=test_client_default)
    client = fastapi.testclient.TestClient(app)
    job_id = "job-1"
    response = client.get(f"/jobs/{job_id}/results")

    assert response.status_code == 200

    exp_body = {"result": f"https://example.org/{job_id}-results.nc"}
    body = response.json()
    assert body == exp_body
