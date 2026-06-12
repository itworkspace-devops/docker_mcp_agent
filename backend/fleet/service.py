from backend.database.repository import (
    get_hosts
)

from backend.client.mcp_client import (
    MCPClient
)

mcp = MCPClient()


def fleet_health():

    result = []

    for host in get_hosts():

        host_status = {

            "host":
                host.name,

            "healthy":
                True,

            "containers":
                0,

            "running":
                0,

            "stopped":
                0,
        }

        try:

            containers = mcp.call(

                "docker_ps",

                host_name=host.name
            )

            container_list = (
                containers.get(
                    "data",
                    []
                )
            )

            host_status[
                "containers"
            ] = len(
                container_list
            )

            for container in container_list:

                if (
                    container[
                        "status"
                    ] == "running"
                ):

                    host_status[
                        "running"
                    ] += 1

                else:

                    host_status[
                        "stopped"
                    ] += 1

        except Exception:

            host_status[
                "healthy"
            ] = False

        result.append(
            host_status
        )

    return result