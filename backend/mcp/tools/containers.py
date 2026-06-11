from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def list_containers(arguments):

    try:

        client = get_docker()

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
                    "image": c.image.tags,
                }
            )

        return success(result)

    except Exception as ex:

        return failure(str(ex))


def inspect_container(arguments):

    try:

        name = arguments["container"]

        container = get_docker().containers.get(name)

        return success(container.attrs)

    except Exception as ex:

        return failure(str(ex))
    

def run_container(arguments):

    try:

        docker_client = get_docker()

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

        name = arguments["container"]

        container = get_docker().containers.get(name)

        container.start()

        return success(
            {
                "container": name,
                "action": "started"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def stop_container(arguments):

    try:

        name = arguments["container"]

        container = get_docker().containers.get(name)

        container.stop()

        return success(
            {
                "container": name,
                "action": "stopped"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def restart_container(arguments):

    try:

        name = arguments["container"]

        container = get_docker().containers.get(name)

        container.restart()

        return success(
            {
                "container": name,
                "action": "restarted"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def remove_container(arguments):

    try:

        name = arguments["container"]

        container = get_docker().containers.get(name)

        container.remove(force=True)

        return success(
            {
                "container": name,
                "action": "removed"
            }
        )

    except Exception as ex:

        return failure(str(ex))


def container_logs(arguments):

    try:

        name = arguments["container"]

        tail = arguments.get(
            "tail",
            100
        )

        container = get_docker().containers.get(name)

        logs = container.logs(
            tail=tail
        ).decode()

        return success(logs)

    except Exception as ex:

        return failure(str(ex))


def container_stats(arguments):

    try:

        name = arguments["container"]

        container = get_docker().containers.get(name)

        stats = container.stats(
            stream=False
        )

        return success(stats)

    except Exception as ex:

        return failure(str(ex))