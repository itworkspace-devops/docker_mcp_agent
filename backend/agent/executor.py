import json

from backend.agent import state
from backend.client.mcp_client import MCPClient

mcp = MCPClient()


def executor(state):

    # tool_data = json.loads(
    #     state["tool_name"]
    # )
    
    tool_name = state["tool_name"]

    tool_args = state.get(
        "tool_args",
        {}
    )

    result = mcp.call(
        tool_name,
        tool_args
    )

    # result = mcp.call(
    #     tool_data["tool_name"],
    #     tool_data["tool_args"]
    # )

    return {
        "result": result
    }