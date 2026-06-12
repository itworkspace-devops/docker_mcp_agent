from fastapi import APIRouter

from backend.drift.service import (
    run_drift_scan
)

router = APIRouter()


@router.post("/scan")
def scan():

    findings = run_drift_scan()

    return {

        "success": True,

        "findings":
            findings
    }