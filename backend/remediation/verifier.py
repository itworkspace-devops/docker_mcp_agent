from backend.client.mcp_client import (
    MCPClient
)

mcp = MCPClient()


def verify_container_running(
    container
):

    result = mcp.call(
        "docker_inspect",
        {
            "container":
                container
        }
    )

    if not result.get(
        "success"
    ):
        return False

    data = result.get(
        "data",
        {}
    )

    state = (
        data.get(
            "State",
            {}
        )
    )

    return (
        state.get(
            "Running",
            False
        )
    )