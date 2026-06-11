from backend.config.settings import settings

from backend.approval.service import (
    request_approval
)

from backend.approval.store import (
    PENDING_APPROVALS
)

from backend.approval.engine import (
    create_execution_id,
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

    # CLI approval mode
    if settings.approval_mode == "cli":

        approved = request_approval(
            tool_name,
            tool_args
        )

        return {
            "approval_required": True,
            "approved": approved,
        }

    # API / Teams approval mode
    execution_id = create_execution_id()

    PENDING_APPROVALS[
        execution_id
    ] = {
        "tool_name": tool_name,
        "tool_args": tool_args,
    }

    return {
        "approval_required": True,
        "approved": False,
        "execution_id": execution_id,
    }