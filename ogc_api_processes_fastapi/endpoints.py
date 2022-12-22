"""Endpoints definition."""

import urllib.parse
from typing import Callable, List, Optional

import fastapi

from . import clients, models


def create_links_to_job(
    request: fastapi.Request, job: models.StatusInfo
) -> List[models.Link]:
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
        models.Link(
            href=urllib.parse.urljoin(str(request.base_url), f"jobs/{job.jobID}"),
            rel=rel_job_link,
            type="application/json",
            title=title_job_link,
        )
    ]
    if job.status.value in ("successful", "failed"):
        links.append(
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"jobs/{job.jobID}/results"
                ),
                rel="results",
            )
        )
    return links


def create_self_link(
    request_url: str, title: Optional[str] = None, type: Optional[str] = None
) -> models.Link:
    self_link = models.Link(href=str(request_url), rel="self")
    if type:
        self_link.type = type
    if title:
        self_link.title = title
    return self_link


def create_page_link(
    request_url: str, page: str, pagination_qs: models.PaginationQueryParameters
) -> models.Link:
    if page not in ("next", "prev"):
        raise ValueError(f"{page} is not a valid value for ``page`` parameter")
    request_parsed = urllib.parse.urlsplit(request_url)
    queries = urllib.parse.parse_qs(request_parsed.query)
    queries_page = queries.copy()
    queries_new = getattr(pagination_qs, page)
    queries_page.update(queries_new)
    query_string = urllib.parse.urlencode(queries_page, doseq=True)
    parsed_page_request = request_parsed._replace(query=query_string)
    url_page = parsed_page_request.geturl()
    link_page = models.Link(href=url_page, rel=page)
    return link_page


def create_pagination_links(
    request_url: str, pagination_qs: Optional[models.PaginationQueryParameters]
) -> List[models.Link]:
    pagination_links = []
    if pagination_qs:
        if pagination_qs.next:
            link_next = create_page_link(request_url, "next", pagination_qs)
            pagination_links.append(link_next)
        if pagination_qs.prev:
            link_prev = create_page_link(request_url, "prev", pagination_qs)
            pagination_links.append(link_prev)
    return pagination_links


def create_get_landing_page_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], models.LandingPage]:
    def get_landing_page(
        request: fastapi.Request,
    ) -> models.LandingPage:
        """Get the API landing page."""
        links = [
            models.Link(
                href=urllib.parse.urljoin(str(request.base_url), "openapi.json"),
                rel="service-desc",
                type="application/vnd.oai.openapi+json;version=3.0",
                title="OpenAPI service description",
            ),
            models.Link(
                href=urllib.parse.urljoin(str(request.base_url), "conformance"),
                rel="http://www.opengis.net/def/rel/ogc/1.0/conformance",
                type="application/json",
                title="Conformance declaration",
            ),
            models.Link(
                href=urllib.parse.urljoin(str(request.base_url), "processes"),
                rel="http://www.opengis.net/def/rel/ogc/1.0/processes",
                type="application/json",
                title="Metadata about the processes",
            ),
        ]
        landing_page = models.LandingPage(links=links)

        return landing_page

    return get_landing_page


def create_get_conformance_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], models.ConfClass]:
    def get_conformance(request: fastapi.Request) -> models.ConfClass:
        """Get the API conformance declaration page."""
        conformance = models.ConfClass(
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
) -> Callable[[fastapi.Request], models.ProcessList]:
    def get_processes(
        request: fastapi.Request,
        process_list: models.ProcessList = fastapi.Depends(client.get_processes),
    ) -> models.ProcessList:
        """Get the list of available processes.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        for process in process_list.processes:
            process.links = [
                models.Link(
                    href=urllib.parse.urljoin(
                        str(request.base_url), f"processes/{process.id}"
                    ),
                    rel="process",
                    type="application/json",
                    title="process description",
                )
            ]
        process_list.links = [
            create_self_link(str(request.url), type="application/json")
        ]
        pagination_links = create_pagination_links(
            str(request.url), process_list._pagination_qs
        )
        for link in pagination_links:
            process_list.links.append(link)

        return process_list

    return get_processes


def create_get_process_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], models.ProcessDescription]:
    def get_process(
        request: fastapi.Request,
        process: models.ProcessDescription = fastapi.Depends(client.get_process),
    ) -> models.ProcessDescription:
        """Get the description of a specific process.

        The list of processes contains a summary of each process
        the OGC API - Processes offers, including the link to a
        more detailed description of the process.
        """
        process.links = [
            create_self_link(str(request.url)),
            models.Link(
                href=urllib.parse.urljoin(
                    str(request.base_url), f"processes/{process.id}/execution"
                ),
                rel="execute",
                type="application/json",
                title="process execution",
            ),
        ]

        return process

    return get_process


def create_post_process_execution_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request, fastapi.Response], models.StatusInfo]:
    def post_process_execution(
        request: fastapi.Request,
        response: fastapi.Response,
        status_info: models.StatusInfo = fastapi.Depends(client.post_process_execution),
    ) -> models.StatusInfo:
        """Create a new job."""
        status_info.links = [
            create_self_link(str(request.url)),
            models.Link(
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

    return post_process_execution


def create_get_jobs_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], models.JobList]:
    def get_jobs(
        request: fastapi.Request,
        job_list: models.JobList = fastapi.Depends(client.get_jobs),
    ) -> models.JobList:
        """Show the list of submitted jobs."""
        for job in job_list.jobs:
            job.links = create_links_to_job(job=job, request=request)
        job_list.links = [
            create_self_link(str(request.url), title="list of submitted jobs"),
        ]
        pagination_links = create_pagination_links(
            str(request.url), job_list._pagination_qs
        )
        for link in pagination_links:
            job_list.links.append(link)

        return job_list

    return get_jobs


def create_get_job_endpoint(
    client: clients.BaseClient,
) -> Callable[[fastapi.Request], models.StatusInfo]:
    def get_job(
        request: fastapi.Request,
        job: models.StatusInfo = fastapi.Depends(client.get_job),
    ) -> models.StatusInfo:
        """Show the status of a job."""
        job.links = create_links_to_job(job=job, request=request)

        return job

    return get_job


def create_get_job_results_endpoint(
    client: clients.BaseClient,
) -> Callable[[], models.Results]:
    def get_job_results(
        job_results: models.Results = fastapi.Depends(client.get_job_results),
    ) -> models.Results:
        """Show results of a job."""
        return job_results

    return get_job_results


def create_delete_job_endpoint(
    client: clients.BaseClient,
) -> Callable[[], models.StatusInfo]:
    def delete_job(
        job: models.StatusInfo = fastapi.Depends(client.delete_job),
    ) -> models.StatusInfo:
        """Cancel a job."""
        return job

    return delete_job


endpoints_generators = {
    "GetLandingPage": create_get_landing_page_endpoint,
    "GetConformance": create_get_conformance_endpoint,
    "GetProcesses": create_get_processes_endpoint,
    "GetProcess": create_get_process_endpoint,
    "PostProcessExecution": create_post_process_execution_endpoint,
    "GetJobs": create_get_jobs_endpoint,
    "GetJob": create_get_job_endpoint,
    "GetJobResults": create_get_job_results_endpoint,
    "DeleteJob": create_delete_job_endpoint,
    "PostProcessExecute": create_post_process_execution_endpoint,
}


def create_endpoint(  # type: ignore
    route_name: str,
    client: clients.BaseClient,
):
    endpoint = endpoints_generators[route_name](client)

    return endpoint
