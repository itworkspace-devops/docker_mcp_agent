from fastapi import APIRouter

from backend.database.repository import (
    get_findings
)

router = APIRouter()


@router.get("")
def findings():

    return get_findings()