from fastapi import APIRouter

from backend.incidents.service import (
    investigate_container
)

router = APIRouter()


@router.get("/{container}")
def investigate(
    container: str
):

    return investigate_container(
        container
    )

@router.get("")
def incidents():

    return [
        {
            "container": "nginx",
            "severity": "critical",
            "root_cause": "Container exited unexpectedly",
            "analysis": "Exit code 137 detected",
            "recommendation": "Restart container and inspect logs"
        }
    ]    