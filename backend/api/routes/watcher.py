from fastapi import APIRouter

from backend.watcher.watcher import (
    run_watcher
)

router = APIRouter()


@router.post("/run")
def run_now():

    run_watcher()

    return {
        "success": True
    }