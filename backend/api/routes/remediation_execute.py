from fastapi import APIRouter

from backend.database.repository import (
    get_remediation_by_id
)

from backend.remediation.executor import (
    execute_remediation
)

router = APIRouter()


@router.post("/{remediation_id}")
def execute(
    remediation_id: int
):

    remediation = get_remediation_by_id(
        remediation_id
    )

    if not remediation:

        return {
            "success": False,
            "error": "Remediation not found"
        }

    return execute_remediation(
        remediation
    )