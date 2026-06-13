from backend.client.mcp_client import MCPClient
from backend.audit.logger import audit_log

mcp = MCPClient()


def executor(state):

    # ==================================================
    # Authorization Check
    # ==================================================

    if not state.get(
        "authorized",
        True
    ):

        return {
            "result":
                state.get(
                    "result",
                    {
                        "success": False,
                        "error": "Unauthorized"
                    }
                )
        }

    # ==================================================
    # Approval Check
    # ==================================================

    if state.get(
        "approval_required",
        False
    ):

        if not state.get(
            "approved",
            False
        ):

            audit_log(
                action=state.get(
                    "tool_name",
                    "unknown"
                ),
                target=str(
                    state.get(
                        "tool_args",
                        {}
                    )
                ),
                status="cancelled",
            )

            return {
                "result": {
                    "success": False,
                    "message": (
                        "Operation cancelled by user."
                    ),
                }
            }

    # ==================================================
    # Execute MCP Tool
    # ==================================================

    tool_name = state["tool_name"]

    tool_args = state.get(
        "tool_args",
        {}
    )

    try:

        host_name = state.get(
            "host_name"
        )

        result = mcp.call(

            tool_name,

            tool_args,

            host_name=host_name
        )

        audit_log(
            action=tool_name,
            target=str(tool_args),
            status="success",
        )

        return {
            "result": result
        }

    except Exception as ex:

        audit_log(
            action=tool_name,
            target=str(tool_args),
            status=f"failed: {str(ex)}",
        )

        return {
            "result": {
                "success": False,
                "error": str(ex),
            }
        }