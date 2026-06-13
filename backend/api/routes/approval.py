from fastapi import APIRouter, HTTPException

from backend.approval.service import (
    resolve_pending_approval,
)

from backend.approval.store import (
    PENDING_APPROVALS,
)

from backend.client.mcp_client import (
    MCPClient
)

router = APIRouter()

mcp = MCPClient()


@router.get("/pending")
def pending():

    results = []

    for execution_id, data in (
        PENDING_APPROVALS.items()
    ):

        if data.get("approved") is not None:
            continue

        results.append({

            "execution_id":
                execution_id,

            **data
        })

    return results

@router.post("/{execution_id}/reject")
def reject(
    execution_id: str
):

    if execution_id not in PENDING_APPROVALS:

        raise HTTPException(
            404,
            "Approval not found"
        )

    approval = PENDING_APPROVALS[
        execution_id
    ]

    if approval.get("origin") == "cli":
        resolve_pending_approval(
            execution_id,
            False,
            "ui",
        )

        return {
            "success": True,
            "execution_id": execution_id,
            "status": "rejected",
        }

    PENDING_APPROVALS.pop(execution_id)

    return {
        "success": True,
        "execution_id": execution_id,
        "status": "rejected",
    }


@router.post("/approve/{execution_id}")
def approve(
    execution_id: str
):

    if execution_id not in PENDING_APPROVALS:

        return {
            "success": False,
            "message": "Not found"
        }

    task = PENDING_APPROVALS[execution_id]

    if task.get("origin") == "cli":
        resolve_pending_approval(
            execution_id,
            True,
            "ui",
        )

        return {
            "success": True,
            "message": "Approval recorded for CLI request.",
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