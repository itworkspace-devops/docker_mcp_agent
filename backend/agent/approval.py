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
    
    
    print("=" * 80)
    print("APPROVAL NODE CALLED")
    print("APPROVAL MODE:", settings.approval_mode)

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
        origin=settings.approval_mode,
    )

    approved = False

    if settings.approval_mode == "cli":

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