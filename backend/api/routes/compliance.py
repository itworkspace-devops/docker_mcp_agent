from fastapi import APIRouter

from backend.compliance.service import (
    run_compliance_scan
)

router = APIRouter()


@router.post("/scan")
def scan():

    return {

        "success": True,

        "results":
            run_compliance_scan()
    }