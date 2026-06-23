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
            if state.get("origin") == "ui":
                # For UI, we return the result from approval_node which contains action='approval_required'
                return {
                    "result": state.get("result")
                }

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

    tool_plan = state.get("tool_plan") or []
    host_name = state.get("host_name")

    def run_tool(tool_name, tool_args):
        try:
            result = mcp.call(tool_name, tool_args, host_name=host_name)
            audit_log(action=tool_name, target=str(tool_args), status="success")
            return result
        except Exception as ex:
            audit_log(action=tool_name, target=str(tool_args), status=f"failed: {str(ex)}")
            return {"success": False, "error": str(ex)}

    if tool_plan:
        outputs = []
        for step in tool_plan:
            tool_name = step["tool_name"]
            tool_args = step.get("tool_args", {})
            result = run_tool(tool_name, tool_args)
            outputs.append({
                "tool_name": tool_name,
                "tool_args": tool_args,
                "result": result,
            })
            if not result.get("success", True):
                break
        return {"result": {"success": True, "message": "Completed multi-step request.", "data": outputs}}

    tool_name = state["tool_name"]
    tool_args = state.get("tool_args", {})
    if host_name and "host_name" not in tool_args:
        tool_args = {**tool_args, "host_name": host_name}
    result = run_tool(tool_name, tool_args)
    return {"result": result}
