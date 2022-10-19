"""Endpoints definition."""

import urllib.parse
from typing import Callable, List, Optional

import fastapi

from . import clients, responses


def create_links_to_job(
    job: responses.StatusInfo, request: fastapi.Request
) -> List[responses.Link]:
    """Create links to attach to provided the job.

    Parameters
    ----------
    job : schema["StatusInfo"]
        Job to create links for.

    Returns
    -------
    List[responses.Link]
        Links to attach to job.
    """
    rel_job_link = "self"
    title_job_link = None
    if not request.path_params:
        rel_job_link = "monitor"
        title_job_link = "job status info"
    links = [
        responses.Link(
            href=urllib.parse.urljoin(str(request.base_url), f"jobs/{job.jobID}"),
            rel=rel_job_link,
            type="application/json",
            title=title_job_link,
        )
    ]
    if job.status.value in ("successful", "failed"):
        links.append(
            responses.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{job.jobID}/results"
                ),
                rel="results",
            )
        )
    return links


def create_self_link(
    request: fastapi.Request, title: Optional[str] = None, type: Optional[str] = None
) -> responses.Link:
    self_link = responses.Link(href=str(request.url), rel="self")
    if type:
        self_link.type = type
    if title:
        self_link.title = title
    return self_link


def create_get_landing_page_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], responses.LandingPage]:
    def get_landing_page(
        request: fastapi.Request,
    ) -> responses.LandingPage:
        """Get the API landing page."""
        links = [
            responses.Link(
                href=urllib.parse.urljoin(str(request.base_url), "openapi.json"),
                rel="service-desc",
                type="application/vnd.oai.openapi+json;version=3.0",
                title="OpenAPI service description",
            ),
            responses.Link(
                href=urllib.parse.urljoin(str(request.base_url), "conformance"),
                rel="http://www.opengis.net/def/rel/ogc/1.0/conformance",
                type="application/json",
                title="Conformance declaration",
            ),
            responses.Link(
                href=urllib.parse.urljoin(str(request.base_url), "processes"),
                rel="http://www.opengis.net/def/rel/ogc/1.0/processes",
                type="application/json",
                title="Metadata about the processes",
            ),
        ]
        landing_page = responses.LandingPage(links=links)

        return landing_page

    return get_landing_page


def create_get_conformance_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], responses.ConfClass]:
    def get_conformance(request: fastapi.Request) -> responses.ConfClass:
        """Get the API conformance declaration page."""
        conformance = responses.ConfClass(
            conformsTo=[
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/job-list",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/json",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/oas30",
            ]
        )

        return conformance

    return get_conformance


def create_get_processes_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], responses.ProcessList]:
    def get_processes(
        request: fastapi.Request,
        process_list: responses.ProcessList = fastapi.Depends(client.get_processes),
    ) -> responses.ProcessList:
        """Get the list of available processes.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        for process in process_list.processes:
            process.links = [
                responses.Link(
                    href=urllib.parse.urljoin(
                        str(request.base_url), f"processes/{process.id}"
                    ),
                    rel="process",
                    type="application/json",
                    title="process description",
                )
            ]
        process_list.links = [create_self_link(request, type="application/json")]

        return process_list

    return get_processes


def create_get_process_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], responses.ProcessDescription]:
    def get_process(
        request: fastapi.Request,
        process: responses.ProcessDescription = fastapi.Depends(client.get_process),
    ) -> responses.ProcessDescription:
        """Get the description of a specific process.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process.links = [
            create_self_link(request),
            responses.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process.id}/execute"
                ),
                rel="execute",
                type="application/json",
                title="process execution",
            ),
        ]

        return process

    return get_process


def create_post_process_execute_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request, fastapi.Response], responses.StatusInfo]:
    def post_process_execute(
        request: fastapi.Request,
        response: fastapi.Response,
        status_info: responses.StatusInfo = fastapi.Depends(
            client.post_process_execute
        ),
    ) -> responses.StatusInfo:
        """Create a new job."""
        status_info.links = [
            create_self_link(request),
            responses.Link(
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

        return status_info

    return post_process_execute


def create_get_jobs_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], responses.JobList]:
    def get_jobs(
        request: fastapi.Request,
        job_list: responses.JobList = fastapi.Depends(client.get_jobs),
    ) -> responses.JobList:
        """Show the list of submitted jobs."""
        for job in job_list.jobs:
            job.links = create_links_to_job(job=job, request=request)
        job_list.links = [create_self_link(request, title="list of submitted jobs")]

        return job_list

    return get_jobs


def create_get_job_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], responses.StatusInfo]:
    def get_job(
        request: fastapi.Request,
        job: responses.StatusInfo = fastapi.Depends(client.get_job),
    ) -> responses.StatusInfo:
        """Show the status of a job."""
        job.links = create_links_to_job(job=job, request=request)

        return job

    return get_job


def create_get_job_results_endpoint(
    client: clients.BaseClient,
) -> Callable[[], responses.Results]:
    def get_job_results(
        job_results: responses.Results = fastapi.Depends(client.get_job_results),
    ) -> responses.Results:
        """Show results of a job."""
        return job_results

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


def create_endpoint(  # type: ignore
    route_name: str,
    client: clients.BaseClient,
):
    endpoint = endpoints_generators[route_name](client)

    return endpoint
