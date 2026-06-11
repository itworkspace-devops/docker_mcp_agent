from fastapi import APIRouter

from backend.client.mcp_client import MCPClient

router = APIRouter()

mcp = MCPClient()


@router.get("/health")
def system_health():

    return mcp.call(
        "docker_ping"
    )


@router.get("/info")
def system_info():

    return mcp.call(
        "docker_info"
    )


@router.get("/version")
def system_version():

    return mcp.call(
        "docker_version"
    )