import json

from backend.agent import state
from backend.client.mcp_client import MCPClient

mcp = MCPClient()


def executor(state):

    tool_data = json.loads(
        state["tool_name"]
    )

    result = mcp.call(
        tool_data["tool_name"],
        tool_data["tool_args"]
    )

    return {
        "result": result
    }