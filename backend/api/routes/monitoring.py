from fastapi import APIRouter

from backend.monitoring.service import (
    run_monitoring
)

from backend.database.repository import (
    get_latest_metrics,
    get_findings,
)

router = APIRouter()


@router.post("/run")
def monitor():

    return run_monitoring()


@router.get("/metrics")
def metrics():

    return get_latest_metrics()


@router.get("/findings")
def findings():

    return get_findings()