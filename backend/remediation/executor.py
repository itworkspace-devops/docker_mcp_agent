from backend.client.mcp_client import MCPClient

from backend.watcher.findings import (
    update_remediation_status,
    close_finding,
)

from backend.audit.logger import (
    audit_log
)

mcp = MCPClient()


def execute_remediation(
    remediation,
):

    remediation_id = remediation["id"]

    finding_id = remediation["finding_id"]

    plan = remediation["plan"]

    try:

        result = mcp.call(
            plan["tool_name"],
            plan["tool_args"]
        )

        update_remediation_status(
            remediation_id,
            "completed"
        )

        close_finding(
            finding_id
        )

        audit_log(
            action=plan["tool_name"],
            target=str(
                plan["tool_args"]
            ),
            status="auto-remediated",
        )

        return result

    except Exception as ex:

        update_remediation_status(
            remediation_id,
            "failed"
        )

        audit_log(
            action=plan["tool_name"],
            target=str(
                plan["tool_args"]
            ),
            status=f"failed: {str(ex)}",
        )

        return {
            "success": False,
            "error": str(ex),
        }
        
def execute_plan(plan):

    tool_name = plan.get(
        "tool_name"
    )

    tool_args = plan.get(
        "tool_args",
        {}
    )

    return mcp.call(
        tool_name,
        tool_args
    )