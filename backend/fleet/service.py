from backend.database.repository import (
    get_hosts
)

from backend.client.mcp_client import (
    MCPClient
)

mcp = MCPClient()


def _count_containers_for_host(host_name=None, host_label="local"):

    host_status = {
        "host": host_label,
        "healthy": True,
        "containers": 0,
        "running": 0,
        "stopped": 0,
    }

    try:
        containers = mcp.call(
            "docker_ps",
            host_name=host_name
        )

        container_list = (
            containers.get(
                "data",
                []
            )
        ) or []

        host_status["containers"] = len(container_list)

        for container in container_list:
            status = str(container.get("status", "")).lower()
            if status == "running" or status.startswith("running"):
                host_status["running"] += 1
            else:
                host_status["stopped"] += 1

    except Exception:
        host_status["healthy"] = False

    return host_status


def fleet_health():

    hosts = get_hosts()

    if not hosts:
        return [
            _count_containers_for_host(
                host_name=None,
                host_label="local"
            )
        ]

    result = []

    for host in hosts:
        host_status = _count_containers_for_host(
            host_name=host.name,
            host_label=host.name,
        )
        result.append(host_status)

    return result