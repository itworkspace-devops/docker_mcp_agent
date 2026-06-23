from fastapi import APIRouter

from backend.database.repository import (
    get_hosts
)

from backend.client.mcp_client import (
    MCPClient
)

from backend.fleet.service import (
    fleet_health
)

router = APIRouter()

mcp = MCPClient()

from backend.database.repository import (
    get_enabled_hosts
)

# ...

@router.get("/hosts")
def fleet_hosts():

    return get_enabled_hosts()


@router.get("/containers")
def fleet_containers():

    result = []

    # Always include local host
    try:
        containers = mcp.call("docker_ps", host_name="local")
        result.append({"host": "local", "containers": containers})
    except Exception as ex:
        result.append({"host": "local", "error": str(ex)})

    hosts = get_enabled_hosts()

    for host in hosts:

        if host.name == "local":
            continue # Already added

        try:
            containers = mcp.call(
                "docker_ps",
                host_name=host.name
            )
            result.append(
                {
                    "host":
                        host.name,
                    "containers":
                        containers
                }
            )
        except Exception as ex:
            result.append(
                {
                    "host":
                        host.name,
                    "error":
                        str(ex)
                }
            )

    return result