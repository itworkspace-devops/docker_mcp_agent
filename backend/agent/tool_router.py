from typing import Optional


def route_query(query: str) -> Optional[dict]:

    query = query.lower().strip()

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
            "tool_name": "docker_ps",
            "tool_args": {}
        }

    # Create Container
    if (
        query.startswith("create ")
        and "container" in query
    ):

        image = (
            query
            .replace("create", "")
            .replace("container", "")
            .strip()
        )

        return {
            "tool_name": "docker_run",
            "tool_args": {
                "image": image
            }
        }

    # Run Container
    if (
        query.startswith("create ")
        and "container" in query
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
            "tool_name": "docker_run",
            "tool_args": {
                "image": image
            }
        }

    # Restart Container
    if query.startswith("restart "):

        container = query.replace(
            "restart ",
            ""
        ).strip()

        return {
            "tool_name": "docker_restart",
            "tool_args": {
                "container": container
            }
        }

    # Stop Container
    if query.startswith("stop "):

        container = query.replace(
            "stop ",
            ""
        ).strip()

        return {
            "tool_name": "docker_stop",
            "tool_args": {
                "container": container
            }
        }

    # Start Existing Container
    if query.startswith("start "):

        container = query.replace(
            "start ",
            ""
        ).strip()

        return {
            "tool_name": "docker_start",
            "tool_args": {
                "container": container
            }
        }

    # Inspect Container
    if query.startswith("inspect "):

        container = query.replace(
            "inspect ",
            ""
        ).strip()

        return {
            "tool_name": "docker_inspect",
            "tool_args": {
                "container": container
            }
        }

    # Container Logs
    if query.startswith("logs "):

        container = query.replace(
            "logs ",
            ""
        ).strip()

        return {
            "tool_name": "docker_logs",
            "tool_args": {
                "container": container,
                "tail": 100
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
            "tool_name": "docker_images",
            "tool_args": {}
        }

    if query.startswith("pull "):

        image = query.replace(
            "pull ",
            ""
        ).strip()

        return {
            "tool_name": "docker_pull",
            "tool_args": {
                "image": image
            }
        }

    if query.startswith("remove image "):

        image = query.replace(
            "remove image ",
            ""
        ).strip()

        return {
            "tool_name": "docker_rmi",
            "tool_args": {
                "image": image,
                "force": False
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
            "tool_name": "docker_info",
            "tool_args": {}
        }

    if query in [
        "docker version",
        "version",
    ]:
        return {
            "tool_name": "docker_version",
            "tool_args": {}
        }

    if query in [
        "ping",
        "health",
        "docker health",
    ]:
        return {
            "tool_name": "docker_ping",
            "tool_args": {}
        }

    return None