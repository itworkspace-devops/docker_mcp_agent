from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def _find_container(query, host_name=None):

    if not query:
        raise ValueError(
            "Container name filter is required"
        )

    query_lower = query.lower()
    client = get_docker(host_name)

    try:
        return client.containers.get(query)
    except Exception:
        pass

    matches = []
    containers = client.containers.list(all=True)

    for c in containers:
        image_tags = c.image.tags or []
        if (
            query_lower in c.name.lower()
            or query_lower in c.short_id.lower()
            or any(query_lower in tag.lower() for tag in image_tags)
        ):
            matches.append(c)

    if len(matches) == 1:
        return matches[0]

    if len(matches) == 0:
        raise ValueError(
            f"No containers matched '{query}'"
        )

    raise ValueError(
        f"Multiple containers matched '{query}': "
        + ", ".join(c.name for c in matches)
    )


def list_containers(arguments):

    try:
        host_name = arguments.get("host_name")
        client = get_docker(host_name)

        containers = client.containers.list(
            all=True
        )

        result = []

        for c in containers:

            result.append(
                {
                    "id": c.short_id,
                    "name": c.name,
                    "status": c.status,
                    "image": c.image.tags or [],
                }
            )

        return success(result)

    except Exception as ex:

        return failure(str(ex))


def grep_containers(arguments):

    try:
        host_name = arguments.get("host_name")
        query = arguments.get(
            "name"
        ) or arguments.get(
            "container"
        )

        if not query:
            return failure(
                "Container name filter is required"
            )

        query_lower = query.lower()
        client = get_docker(host_name)

        containers = client.containers.list(
            all=True
        )

        matches = []

        for c in containers:
            image_tags = c.image.tags or []
            if (
                query_lower in c.name.lower()
                or query_lower in c.short_id.lower()
                or any(query_lower in tag.lower() for tag in image_tags)
            ):
                matches.append(
                    {
                        "id": c.short_id,
                        "name": c.name,
                        "status": c.status,
                        "image": image_tags,
                    }
                )

        return success(matches)

    except Exception as ex:

        return failure(str(ex))


def inspect_container(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        container = _find_container(name, host_name)

        return success(container.attrs)

    except Exception as ex:

        return failure(str(ex))
    

def run_container(arguments):

    try:
        host_name = arguments.get("host_name")
        docker_client = get_docker(host_name)

        image = arguments["image"]

        name = arguments.get(
            "name"
        )

        detach = arguments.get(
            "detach",
            True
        )

        container = docker_client.containers.run(
            image=image,
            name=name,
            detach=detach,
        )

        return success(
            {
                "id": container.short_id,
                "name": container.name,
                "image": image,
            }
        )

    except Exception as ex:

        return failure(str(ex))


def start_container(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        container = _find_container(name, host_name)

        container.start()

        return success(
            {
                "container": container.name,
                "action": "started"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def stop_container(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        container = _find_container(name, host_name)

        container.stop()

        return success(
            {
                "container": container.name,
                "action": "stopped"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def restart_container(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        container = _find_container(name, host_name)

        container.restart()

        return success(
            {
                "container": container.name,
                "action": "restarted"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def remove_container(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        container = _find_container(name, host_name)

        container.remove(force=True)

        return success(
            {
                "container": container.name,
                "action": "removed"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def container_logs(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        tail = arguments.get(
            "tail",
            100
        )

        container = _find_container(name, host_name)

        logs = container.logs(
            tail=tail
        ).decode()

        return success(logs)

    except Exception as ex:

        return failure(str(ex))


def container_stats(arguments):

    try:
        host_name = arguments.get("host_name")
        name = arguments["container"]

        container = _find_container(name, host_name)

        stats = container.stats(
            stream=False
        )

        return success(stats)

    except Exception as ex:

        return failure(str(ex))