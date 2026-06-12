from backend.mcp.docker_client import (
    get_docker
)


def check_stopped_containers():

    findings = []

    client = get_docker()

    containers = client.containers.list(
        all=True
    )

    for c in containers:

        if c.status == "exited":

            findings.append(
                {
                    "container":
                    c.name,

                    "status":
                    c.status,
                }
            )

    return findings