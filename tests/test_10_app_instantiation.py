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

import fastapi.testclient

import ogc_api_processes_fastapi


def test_include_ogc_api_processes_routers(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = fastapi.FastAPI()
    app = ogc_api_processes_fastapi.include_routers(app=app, client=test_client)
    routes_path = [app.routes[i].path for i in range(len(app.routes))]

    assert "/processes" in routes_path
    assert "/processes/{process_id}" in routes_path
    assert "/processes/{process_id}/execute" in routes_path
    assert "/jobs" in routes_path
    assert "/jobs/{job_id}" in routes_path
    assert "/jobs/{job_id}/results" in routes_path


def test_instantiate_ogc_api_processes_app(
    test_client: ogc_api_processes_fastapi.BaseClient,
) -> None:
    app = ogc_api_processes_fastapi.instantiate_app(client=test_client)
    routes_path = [app.routes[i].path for i in range(len(app.routes))]

    assert "/processes" in routes_path
    assert "/processes/{process_id}" in routes_path
    assert "/processes/{process_id}/execute" in routes_path
    assert "/jobs" in routes_path
    assert "/jobs/{job_id}" in routes_path
    assert "/jobs/{job_id}/results" in routes_path
