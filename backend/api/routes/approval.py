from fastapi import APIRouter

from backend.approval.store import (
    PENDING_APPROVALS
)

from backend.client.mcp_client import (
    MCPClient
)

router = APIRouter()

mcp = MCPClient()


@router.get("/pending")
def pending():

    return PENDING_APPROVALS


@router.post("/approve/{execution_id}")
def approve(
    execution_id: str
):

    if execution_id not in PENDING_APPROVALS:

        return {
            "success": False,
            "message": "Not found"
        }

    task = PENDING_APPROVALS.pop(
        execution_id
    )

    result = mcp.call(
        task["tool_name"],
        task["tool_args"]
    )

    return {
        "success": True,
        "result": result
    }