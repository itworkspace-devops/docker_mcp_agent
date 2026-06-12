from backend.client.mcp_client import MCPClient

mcp = MCPClient()


def collect_diagnostics(
    container
):

    data = {}

    data["inspect"] = mcp.call(
        "docker_inspect",
        {
            "container":
                container
        }
    )

    data["logs"] = mcp.call(
        "docker_logs",
        {
            "container":
                container,
            "tail":
                200
        }
    )

    return data