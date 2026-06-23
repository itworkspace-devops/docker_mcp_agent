from backend.config.settings import settings

from backend.approval.service import (
    create_pending_approval,
    remove_pending_approval,
    request_approval,
)

from backend.approval.engine import (
    requires_approval,
)


def approval_node(state):
    
    origin = state.get("origin", "cli")
    
    print("=" * 80)
    print("APPROVAL NODE CALLED")
    print("ORIGIN:", origin)

    tool_name = state["tool_name"]
    
    print("TOOL:", tool_name)
    print("REQUIRES APPROVAL:", requires_approval(tool_name))

    tool_args = state.get(
        "tool_args",
        {}
    )

    if not requires_approval(tool_name):

        return {
            "approval_required": False,
            "approved": True,
        }

    execution_id = create_pending_approval(
        tool_name,
        tool_args,
        origin=origin,
        host_name=state.get("host_name")
    )

    approved = False

    if origin == "cli":

        approved = request_approval(
            tool_name,
            tool_args,
            execution_id=execution_id,
        )

        remove_pending_approval(execution_id)
        
        return {
            "approval_required": True,
            "approved": approved,
            "execution_id": execution_id,
        }

    # For UI, we return immediately with approval_required=True
    # The executor node will check if it's approved.
    # But wait, if we return from approval_node, the graph continues to executor.
    # We need to make sure the graph STOPS if approval is required but not yet given (for UI).
    
    return {
        "approval_required": True,
        "approved": False,
        "execution_id": execution_id,
        "result": {
            "success": True,
            "action": "approval_required",
            "execution_id": execution_id,
            "tool_name": tool_name,
            "tool_args": tool_args,
            "message": f"Approval required for {tool_name}"
        }
    }