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

from typing import Any, Dict, List

import pytest

import ogc_api_processes_fastapi


def equal_dicts(d1: Dict[str, Any], d2: Dict[str, Any], ignore_keys: List[Any]) -> bool:
    ignored = set(ignore_keys)
    for k1, v1 in d1.items():
        if k1 not in ignored and (k1 not in d2 or d2[k1] != v1):
            return False
    for k2, v2 in d2.items():
        if k2 not in ignored and k2 not in d1:
            return False
    return True


def test_set_resp_model_get_landing_page_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetLandingPage"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.LandingPage
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert equal_dicts(resp_model_schema, exp_resp_model_schema, ["title"])


def test_set_resp_model_get_conformance_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetConformance"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.ConfClass
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert equal_dicts(resp_model_schema, exp_resp_model_schema, ["title"])


def test_set_resp_model_get_process_list_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetProcesses"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.ProcessList
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert resp_model_schema["properties"] == exp_resp_model_schema["properties"]
    assert (
        "links" in resp_model_schema["required"]
        and "links" not in exp_resp_model_schema["required"]
    )


def test_set_resp_model_get_process_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetProcess"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.ProcessDescription
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert equal_dicts(resp_model_schema, exp_resp_model_schema, ["title"])


def test_set_resp_model_post_process_execution_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "PostProcessExecution"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.StatusInfo
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert equal_dicts(resp_model_schema, exp_resp_model_schema, ["title"])


def test_set_resp_model_get_jobs_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetJobs"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.JobList
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert resp_model_schema["properties"] == exp_resp_model_schema["properties"]
    assert (
        "links" in resp_model_schema["required"]
        and "links" not in exp_resp_model_schema["required"]
    )


def test_set_resp_model_get_job_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:

    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetJob"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.StatusInfo
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert equal_dicts(resp_model_schema, exp_resp_model_schema, ["title"])


@pytest.mark.skip(reason="to be inspected")
def test_set_resp_model_get_jobs_results_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    resp_model = ogc_api_processes_fastapi.main.set_response_model(
        test_client_default, "GetJobResults"
    )
    exp_resp_model = ogc_api_processes_fastapi.responses.Results
    resp_model_schema = resp_model.schema()
    exp_resp_model_schema = exp_resp_model.schema()
    assert equal_dicts(resp_model_schema, exp_resp_model_schema, ["title"])


def test_instantiate_app_default(
    test_client_default: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client_default)
    routes_path = [app.routes[i].path for i in range(len(app.routes))]  # type: ignore

    assert "/processes" in routes_path
    assert "/processes/{process_id}" in routes_path
    assert "/processes/{process_id}/execution" in routes_path
    assert "/jobs" in routes_path
    assert "/jobs/{job_id}" in routes_path
    assert "/jobs/{job_id}/results" in routes_path

    openapi_schema = app.openapi()
    assert (
        "metadata"
        not in openapi_schema["components"]["schemas"]["StatusInfo"][
            "properties"
        ].keys()
    )


def test_instantiate_app_extended(
    test_client_extended: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client_extended)
    routes_path = [app.routes[i].path for i in range(len(app.routes))]  # type: ignore

    assert "/processes" in routes_path
    assert "/processes/{process_id}" in routes_path
    assert "/processes/{process_id}/execution" in routes_path
    assert "/jobs" in routes_path
    assert "/jobs/{job_id}" in routes_path
    assert "/jobs/{job_id}/results" in routes_path

    openapi_schema = app.openapi()
    assert (
        "metadata"
        in openapi_schema["components"]["schemas"]["StatusInfo"]["properties"].keys()
    )
