"""Endpoints definition."""

import urllib.parse
from typing import Any, Callable, Dict, List

import fastapi
import pydantic

from . import clients


def make_links_to_job(
    job: Dict[str, Any], request: fastapi.Request
) -> List[Dict[str, Any]]:
    """Create links to attach to provided the job.

    Parameters
    ----------
    job : models.StatusInfo
        Job to create links for.

    Returns
    -------
    List[models.Link]
        Links to attach to job.
    """
    rel_job_link = "self"
    title_job_link = None
    if not request.path_params:
        rel_job_link = "monitor"
        title_job_link = "job status info"
    links = [
        {
            "href": urllib.parse.urljoin(str(request.base_url), f"jobs/{job['jobID']}"),
            "rel": rel_job_link,
            "type": "application/json",
            "title": title_job_link,
        }
    ]
    if job["status"] in ("successful", "failed"):
        links.append(
            {
                "href": urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{job['jobID']}/results"
                ),
                "rel": "results",
            }
        )
    return links


def create_self_link(request: fastapi.Request) -> Dict[str, Any]:
    self_link = {"href": str(request.url), "rel": "self"}
    return self_link


def create_get_landing_page_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    def get_landing_page(request: fastapi.Request) -> response_schema:
        """Get the API landing page."""
        links = [
            {
                "href": urllib.parse.urljoin(str(request.base_url), "openapi.json"),
                "rel": "service-desc",
                "type": "application/vnd.oai.openapi+json;version=3.0",
                "title": "OpenAPI service description",
            },
            {
                "href": urllib.parse.urljoin(str(request.base_url), "conformance"),
                "rel": "http://www.opengis.net/def/rel/ogc/1.0/conformance",
                "type": "application/json",
                "title": "Conformance declaration",
            },
            {
                "href": urllib.parse.urljoin(str(request.base_url), "processes"),
                "rel": "http://www.opengis.net/def/rel/ogc/1.0/processes",
                "type": "application/json",
                "title": "Metadata about the processes",
            },
        ]
        response_body = response_schema(links=links)

        return response_body

    return get_landing_page


def create_get_conformance_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    def get_conformance(request: fastapi.Request) -> response_schema:
        """Get the API conformance declaration page."""
        response_body = response_schema(
            conformsTo=[
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/job-list",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/json",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/oas30",
            ]
        )

        return response_body

    return get_conformance


def create_get_processes_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    def get_processes(
        request: fastapi.Request, processes=fastapi.Depends(client.get_processes)
    ) -> response_schema:
        """Get the list of available processes.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        for process in processes:
            process["links"] = [
                {
                    "href": urllib.parse.urljoin(
                        str(request.base_url), f"processes/{process['id']}"
                    ),
                    "rel": "process",
                    "type": "application/json",
                    "title": "process description",
                }
            ]
        links = [
            {
                "href": urllib.parse.urljoin(str(request.base_url), "processes/"),
                "rel": "self",
                "type": "application/json",
            }
        ]
        response_body = {"processes": processes, "links": links}

        return response_body

    return get_processes


def create_get_process_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    def get_process(
        request: fastapi.Request, process=fastapi.Depends(client.get_process)
    ) -> response_schema:
        """Get the description of a specific process.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process["links"] = [
            {
                "href": urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process['id']}"
                ),
                "rel": "self",
                "type": "application/json",
            },
            {
                "href": urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process['id']}/execute"
                ),
                "rel": "execute",
                "type": "application/json",
                "title": "process execution",
            },
        ]

        response_body = process

        return response_body

    return get_process


def create_post_process_execute_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    def post_process_execute(
        request: fastapi.Request,
        process_id: str,
        response: fastapi.Response,
        status_info=fastapi.Depends(client.post_process_execute),
    ) -> Dict[str, Any]:
        """Create a new job."""
        status_info["links"] = [
            {
                "href": urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process_id}/execute"
                ),
                "rel": "self",
                "type": "application/json",
            },
            {
                "href": urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{status_info['jobID']}"
                ),
                "rel": "monitor",
                "type": "application/json",
                "title": "job status info",
            },
        ]
        response.headers["Location"] = urllib.parse.urljoin(
            str(request.base_url), f"jobs/{status_info['jobID']}"
        )

        return status_info

    return post_process_execute


def create_get_jobs_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    """Add to the provided `router` the `GET /jobs` endpoint.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs` endpoint.
    """

    def get_jobs(
        request: fastapi.Request, jobs_list=fastapi.Depends(client.get_jobs)
    ) -> Any:
        """Show the list of submitted jobs."""
        for job in jobs_list:
            job["links"] = make_links_to_job(job=job, request=request)
        jobs = {
            "jobs": jobs_list,
            "links": [
                {
                    "href": urllib.parse.urljoin(str(request.base_url), "jobs"),
                    "rel": "self",
                    "type": "application/json",
                    "title": "list of submitted jobs",
                }
            ],
        }

        return jobs

    return get_jobs


def create_get_job_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    """Add to the provided `router` the `GET /jobs/{job_id}` endpoint.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs/{job_id}` endpoint.
    """

    def get_job(
        request: fastapi.Request, job=fastapi.Depends(client.get_job)
    ) -> Dict[str, Any]:
        """Show the status of a job."""
        job["links"] = make_links_to_job(job=job, request=request)

        return job

    return get_job


def create_get_job_results_endpoint(
    client: clients.BaseClient, response_schema: pydantic.BaseModel
) -> Callable:
    """Add to the provided `router` the `GET /jobs/{job_id}/results` endpoint.

    Parameters
    ----------
    router : fastapi.APIRouter
        Router to which the endpoint should be added.
    client : clients.BaseClient
        Client implementing the `GET /jobs/{job_id}/results` endpoint.
    """

    def get_job_results(
        job_results=fastapi.Depends(client.get_job_results),
    ) -> Dict[str, Any]:
        """Show results of a job."""
        response = job_results
        return response

    return get_job_results


endpoints_generators = {
    "GetLandingPage": create_get_landing_page_endpoint,
    "GetConformance": create_get_conformance_endpoint,
    "GetProcesses": create_get_processes_endpoint,
    "GetProcess": create_get_process_endpoint,
    "PostProcessExecute": create_post_process_execute_endpoint,
    "GetJobs": create_get_jobs_endpoint,
    "GetJob": create_get_job_endpoint,
    "GetJobResults": create_get_job_results_endpoint,
}


def create_endpoint(
    route_name: str, client: clients.BaseClient, schema: Dict[str, Any]
) -> Callable:
    endpoint = endpoints_generators[route_name](client, schema)

    return endpoint
