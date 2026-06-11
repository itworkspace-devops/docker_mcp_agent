from fastapi import APIRouter

from backend.mcp.registry import (
    get_registered_tools
)

router = APIRouter()


@router.get("")
def list_tools():

    return {
        "tools": get_registered_tools()
    }