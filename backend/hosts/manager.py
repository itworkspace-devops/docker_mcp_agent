import docker

from backend.hosts.registry import (
    HOSTS
)


def get_host_client(
    host_name
):

    host = HOSTS.get(
        host_name
    )

    if not host:

        raise Exception(
            f"Host {host_name} not found"
        )

    return docker.DockerClient(
        base_url=host[
            "docker_host"
        ]
    )