from fastapi import APIRouter

from backend.database.repository import (
    get_enabled_hosts,
    get_findings,
    get_remediations,
)

from backend.drift.service import (
    run_drift_scan,
)

from backend.fleet.service import (
    fleet_health,
)

from backend.api.routes.incidents import (
    incidents as get_incidents,
)

router = APIRouter()


@router.get("/summary")
def summary():

    hosts = get_enabled_hosts()

    findings = get_findings()

    remediations = get_remediations()

    health = fleet_health()

    total_containers = sum(
        host.get("containers", 0)
        for host in health
    )

    running = sum(
        host.get("running", 0)
        for host in health
    )

    stopped = sum(
        host.get("stopped", 0)
        for host in health
    )

    try:
        drift_findings = len(run_drift_scan())
    except Exception:
        drift_findings = 0

    try:
        incident_count = len(get_incidents())
    except Exception:
        incident_count = 0

    return {

        "hosts":
            len(health),

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

        "incidents":
            incident_count,

        "drift_findings":
            drift_findings,
    }