"""Endpoints definition."""

import urllib.parse
from typing import Callable, List

import fastapi

from . import clients, config
from .responses import schema


def create_links_to_job(
    job: schema["StatusInfo"], request: fastapi.Request  # noqa
) -> List[schema["Link"]]:  # noqa
    """Create links to attach to provided the job.

    Parameters
    ----------
    job : schema["StatusInfo"]
        Job to create links for.

    Returns
    -------
    List[schema["Link"]]
        Links to attach to job.
    """
    rel_job_link = "self"
    title_job_link = None
    if not request.path_params:
        rel_job_link = "monitor"
        title_job_link = "job status info"
    links = [
        schema["Link"](
            href=urllib.parse.urljoin(str(request.base_url), f"jobs/{job.jobID}"),
            rel=rel_job_link,
            type="application/json",
            title=title_job_link,
        )
    ]
    if job.status in ("successful", "failed"):
        links.append(
            schema["Link"](
                href=urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{job.jobID}/results"
                ),
                rel="results",
            )
        )
    return links


def create_self_link(
    request: fastapi.Request, title: str = None
) -> schema["Link"]:  # noqa
    self_link = schema["Link"](href=str(request.url), rel="self")
    if title:
        self_link.title = title
    return self_link


def create_get_landing_page_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetLandingPage"]["response_model"]]

    def get_landing_page(
        request: fastapi.Request,
    ) -> response_schema:
        """Get the API landing page."""
        links = [
            schema["Link"](
                href=urllib.parse.urljoin(str(request.base_url), "openapi.json"),
                rel="service-desc",
                type="application/vnd.oai.openapi+json;version=3.0",
                title="OpenAPI service description",
            ),
            schema["Link"](
                href=urllib.parse.urljoin(str(request.base_url), "conformance"),
                rel="http://www.opengis.net/def/rel/ogc/1.0/conformance",
                type="application/json",
                title="Conformance declaration",
            ),
            schema["Link"](
                href=urllib.parse.urljoin(str(request.base_url), "processes"),
                rel="http://www.opengis.net/def/rel/ogc/1.0/processes",
                type="application/json",
                title="Metadata about the processes",
            ),
        ]
        response_body = response_schema(links=links)

        return response_body

    return get_landing_page


def create_get_conformance_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetConformance"]["response_model"]]

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
    client: clients.BaseClient,
) -> Callable:
    response_schema = schema[config.ROUTES["GetProcesses"]["response_model"]]

    def get_processes(
        request: fastapi.Request, processes=fastapi.Depends(client.get_processes)
    ) -> response_schema:
        """Get the list of available processes.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        for process in processes:
            process.links = [
                schema["Link"](
                    href=urllib.parse.urljoin(
                        str(request.base_url), f"processes/{process.id}"
                    ),
                    rel="process",
                    type="application/json",
                    title="process description",
                )
            ]
        links = [
            schema["Link"](
                href=urllib.parse.urljoin(str(request.base_url), "processes/"),
                rel="self",
                type="application/json",
            )
        ]
        response_body = response_schema(processes=processes, links=links)

        return response_body

    return get_processes


def create_get_process_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetProcess"]["response_model"]]

    def get_process(
        request: fastapi.Request, process=fastapi.Depends(client.get_process)
    ) -> response_schema:
        """Get the description of a specific process.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process.links = [
            create_self_link(request),
            schema["Link"](
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process.id}/execute"
                ),
                rel="execute",
                type="application/json",
                title="process execution",
            ),
        ]

        response_body = process

        return response_body

    return get_process


def create_post_process_execute_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetProcess"]["response_model"]]

    def post_process_execute(
        request: fastapi.Request,
        response: fastapi.Response,
        status_info=fastapi.Depends(client.post_process_execute),
    ) -> response_schema:
        """Create a new job."""
        status_info.links = [
            create_self_link(request),
            schema["Link"](
                href=urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{status_info.jobID}"
                ),
                rel="monitor",
                type="application/json",
                title="job status info",
            ),
        ]
        response.headers["Location"] = urllib.parse.urljoin(
            str(request.base_url), f"jobs/{status_info.jobID}"
        )
        response_body = status_info

        return response_body

    return post_process_execute


def create_get_jobs_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetJobs"]["response_model"]]

    def get_jobs(
        request: fastapi.Request, job_list=fastapi.Depends(client.get_jobs)
    ) -> response_schema:
        """Show the list of submitted jobs."""
        for job in job_list:
            job.links = create_links_to_job(job=job, request=request)
        jobs = {
            "jobs": job_list,
            "links": [create_self_link(request, title="list of submitted jobs")],
        }
        response_body = response_schema(**jobs)

        return response_body

    return get_jobs


def create_get_job_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetJob"]["response_model"]]

    def get_job(
        request: fastapi.Request, job=fastapi.Depends(client.get_job)
    ) -> response_schema:
        """Show the status of a job."""
        job.links = create_links_to_job(job=job, request=request)
        response_body = job

        return response_body

    return get_job


def create_get_job_results_endpoint(client: clients.BaseClient) -> Callable:
    response_schema = schema[config.ROUTES["GetJobResults"]["response_model"]]

    def get_job_results(
        job_results=fastapi.Depends(client.get_job_results),
    ) -> response_schema:
        """Show results of a job."""
        response_body = job_results
        return response_body

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


def create_endpoint(route_name: str, client: clients.BaseClient) -> Callable:
    endpoint = endpoints_generators[route_name](client)

    return endpoint
