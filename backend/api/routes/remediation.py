from fastapi import APIRouter

from backend.database.repository import (
    get_remediations
)

router = APIRouter()


@router.get("")
def remediations():

    return get_remediations()