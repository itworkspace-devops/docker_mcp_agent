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


@router.get("/health")
def health():

    return fleet_health()

@router.get("/hosts")
def fleet_hosts():

    return get_hosts()


@router.get("/containers")
def fleet_containers():

    result = []

    for host in get_hosts():

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