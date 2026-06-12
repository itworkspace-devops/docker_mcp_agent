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