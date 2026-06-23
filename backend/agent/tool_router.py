from typing import Optional


def extract_host(query):

    if " on " not in query:
        return query, None

    parts = query.rsplit(
        " on ",
        1
    )

    return (
        parts[0].strip(),
        parts[1].strip()
    )
    

def _is_dockerfile_compose_request(query: str) -> bool:
    return any(
        keyword in query
        for keyword in [
            "dockerfile",
            "docker-compose",
            "docker compose",
            "compose",
        ]
    )


def route_query(
    query: str
) -> Optional[dict]:

    query = query.lower().strip()

    query, host_name = extract_host(
        query
)

    # ==================================================
    # Monitoring
    # ==================================================

    if query in [

        "show metrics",

        "metrics",

        "docker metrics",

        "container metrics",

        "show container metrics",
    ]:

        return {

            "tool_name":
                "docker_metrics",

            "tool_args":
                {},
        }

    if query in [

        "show cpu usage",

        "cpu usage",

        "container cpu",

        "cpu",
    ]:

        return {

            "tool_name":
                "docker_metrics",

            "tool_args": {

                "metric":
                    "cpu"
            },
        }

    if query in [

        "show memory usage",

        "memory usage",

        "container memory",

        "memory",
    ]:

        return {

            "tool_name":
                "docker_metrics",

            "tool_args": {

                "metric":
                    "memory"
            },
        }

    if query in [

        "show top containers",

        "top containers",

        "top consumers",
    ]:

        return {

            "tool_name":
                "docker_top",

            "tool_args":
                {},
        }

    if query in [

        "show unhealthy containers",

        "unhealthy containers",

        "containers health",
    ]:

        return {

            "tool_name":
                "docker_unhealthy",

            "tool_args":
                {},
        }

    # ==================================================
    # Containers
    # ==================================================

    if query in [

        "containers",

        "list containers",

        "show containers",

        "show running containers",

        "running containers",
    ]:

        return {

            "tool_name":
                "docker_ps",

            "tool_args":
                {},
        }

    # ==================================================
    # Create / Run Container
    # ==================================================

    if (
        query.startswith("create ")
        and "container" in query
        and not any(
            keyword in query
            for keyword in [
                "dockerfile",
                "docker-compose",
                "docker compose",
                "compose",
            ]
        )
    ):

        image = (

            query
            .replace("create", "")
            .replace("container", "")
            .replace("an", "")
            .replace("a", "")
            .strip()
        )

        return {

            "tool_name":
                "docker_run",

            "tool_args": {

                "image":
                    image
            }
        }


    if query == "scan compliance":

        return {

            "tool_name":
                "compliance_scan",

            "tool_args": {}
        }

    if query == "scan drift":

        return {

            "tool_name":
                "drift_scan",

            "tool_args": {}
        }

    if query.startswith(
        "investigate "
    ):

        container = (
            query.replace(
                "investigate ",
                ""
            )
            .replace(
                "container",
                ""
            )
            .strip()
        )

        return {

            "tool_name":
                "incident_investigate",

            "tool_args": {

                "container":
                    container
            }
        } 
        
    if query.startswith(
        "investigate "
    ):

        container = (
            query.replace(
                "investigate ",
                ""
            )
            .strip()
        )

        return {

            "tool_name":
                "incident_investigate",

            "tool_args": {

                "container":
                    container
            }
        }    

    if query.startswith("run ") and not any(
        keyword in query
        for keyword in [
            "dockerfile",
            "docker-compose",
            "docker compose",
            "compose",
            "build",
            "generate",
        ]
    ):

        image = query.replace(
            "run ",
            ""
        ).strip()

        return {

            "tool_name":
                "docker_run",

            "tool_args": {

                "image":
                    image
            }
        }

    # ==================================================
    # Container Actions
    # ==================================================

    if query.startswith("restart ") and not _is_dockerfile_compose_request(query):

        container = query.replace(
            "restart ",
            ""
        ).strip()

        container = (
            container
            .replace("container", "")
            .strip()
        )

        return {

            "tool_name":
                "docker_restart",

            "tool_args": {

                "container":
                    container
            }
        }

    if query.startswith("stop ") and not _is_dockerfile_compose_request(query):

        container = query.replace(
            "stop ",
            ""
        ).strip()

        container = (
            container
            .replace("container", "")
            .strip()
        )

        return {

            "tool_name":
                "docker_stop",

            "tool_args": {

                "container":
                    container
            }
        }

    if query.startswith("start ") and not _is_dockerfile_compose_request(query):

        container = query.replace(
            "start ",
            ""
        ).strip()

        container = (
            container
            .replace("container", "")
            .strip()
        )

        return {

            "tool_name":
                "docker_start",

            "tool_args": {

                "container":
                    container
            }
        }

    if query.startswith("inspect ") and not _is_dockerfile_compose_request(query):

        container = query.replace(
            "inspect ",
            ""
        ).strip()

        return {

            "tool_name":
                "docker_inspect",

            "tool_args": {

                "container":
                    container
            }
        }

    if query.startswith("logs ") and not _is_dockerfile_compose_request(query):

        container = query.replace(
            "logs ",
            ""
        ).strip()

        return {

            "tool_name":
                "docker_logs",

            "tool_args": {

                "container":
                    container,

                "tail":
                    100
            }
        }

    # ==================================================
    # Images
    # ==================================================

    if query in [

        "images",

        "list images",

        "show images",

        "docker images",
    ]:

        return {

            "tool_name":
                "docker_images",

            "tool_args":
                {},
        }

    if query.startswith("pull "):

        image = query.replace(
            "pull ",
            ""
        ).strip()

        return {

            "tool_name":
                "docker_pull",

            "tool_args": {

                "image":
                    image
            }
        }

    if query.startswith(
        "remove image "
    ):

        image = query.replace(
            "remove image ",
            ""
        ).strip()

        return {

            "tool_name":
                "docker_rmi",

            "tool_args": {

                "image":
                    image,

                "force":
                    False
            }
        }

    # ==================================================
    # Docker System
    # ==================================================

    if query in [

        "docker info",

        "info",

        "system info",
    ]:

        return {

            "tool_name":
                "docker_info",

            "tool_args":
                {},
        }

    if query in [

        "docker version",

        "version",
    ]:

        return {

            "tool_name":
                "docker_version",

            "tool_args":
                {},
        }

    if query in [

        "ping",

        "health",

        "docker health",
    ]:

        return {

            "tool_name":
                "docker_ping",

            "tool_args":
                {},
        }

    if "crash loop" in query or "restart loop" in query:
        return {
            "tool_name": "detect_crash_loop",
            "tool_args": {}
        }

    if "oom" in query or "out of memory" in query:
        return {
            "tool_name": "detect_oom_containers",
            "tool_args": {}
        }

    if "port conflict" in query or "port collision" in query:
        return {
            "tool_name": "detect_port_conflicts",
            "tool_args": {}
        }

    if "free port" in query:
        return {
            "tool_name": "find_free_port",
            "tool_args": {}
        }

    return None
