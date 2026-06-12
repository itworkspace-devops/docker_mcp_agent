from fastapi import APIRouter

from backend.database.repository import (
    get_hosts,
    get_latest_metrics,
    get_findings,
    get_remediations,
)

router = APIRouter()


@router.get("/summary")
def summary():

    hosts = get_hosts()

    metrics = get_latest_metrics()

    findings = get_findings()

    remediations = get_remediations()

    total_containers = len(metrics)

    running = len([
        m
        for m in metrics
        if getattr(
            m,
            "status",
            ""
        ) == "running"
    ])

    stopped = len([
        m
        for m in metrics
        if getattr(
            m,
            "status",
            ""
        ) != "running"
    ])

    return {

        "hosts":
            len(hosts),

        "containers":
            total_containers,

        "running":
            running,

        "stopped":
            stopped,

        "findings":
            len(findings),

        "remediations":
            len(remediations),
    }