import docker

from .config import settings

_client = None

def get_docker():

    global _client

    if _client is None:

        _client = docker.DockerClient(
            base_url=settings.docker_host
        )

    return _client