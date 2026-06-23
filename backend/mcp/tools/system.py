from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def docker_info(arguments):
    try:
        host_name = arguments.get("host_name")
        client = get_docker(host_name)
        info = client.info()
        return success(
            {
                "server_version": info.get("ServerVersion"),
                "containers": info.get("Containers"),
                "containers_running": info.get("ContainersRunning"),
                "containers_paused": info.get("ContainersPaused"),
                "containers_stopped": info.get("ContainersStopped"),
                "images": info.get("Images"),
                "operating_system": info.get("OperatingSystem"),
                "architecture": info.get("Architecture"),
                "cpus": info.get("NCPU"),
                "memory": info.get("MemTotal"),
            }
        )
    except Exception as ex:
        return failure(str(ex))


def docker_ping(arguments):
    try:
        host_name = arguments.get("host_name")
        client = get_docker(host_name)
        result = client.ping()
        return success(
            {
                "ping": result,
                "status": "healthy"
            }
        )
    except Exception as ex:
        return failure(str(ex))


def docker_version(arguments):
    try:
        host_name = arguments.get("host_name")
        client = get_docker(host_name)
        version = client.version()
        return success(
            {
                "version": version.get("Version"),
                "api_version": version.get("ApiVersion"),
                "min_api_version": version.get("MinAPIVersion"),
                "git_commit": version.get("GitCommit"),
                "go_version": version.get("GoVersion"),
                "os": version.get("Os"),
                "arch": version.get("Arch"),
                "kernel_version": version.get("KernelVersion"),
            }
        )
    except Exception as ex:
        return failure(str(ex))