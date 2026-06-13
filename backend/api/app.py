from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.docker_agent import (
    router as docker_router
)

from backend.api.routes.system import (
    router as system_router
)

from backend.api.routes.tools import (
    router as tools_router
)

from backend.api.routes.approval import (
    router as approval_router
)

from backend.api.routes.audit import (
    router as audit_router
)

from backend.api.routes.watcher import (
    router as watcher_router
)

from backend.api.routes.findings import (
    router as findings_router
)

from backend.api.routes.remediation import (
    router as remediation_router
)

from backend.api.routes.remediation_execute import (
    router as remediation_execute_router
)

from backend.api.routes.monitoring import (
    router as monitoring_router
)

from backend.monitoring.scheduler import (
    start_scheduler
)

from backend.api.routes.dashboard import (
    router as dashboard_router
)

from backend.api.routes.incidents import (
    router as incidents_router
)

from backend.api.routes.hosts import (
    router as hosts_router
)

from backend.api.routes.fleet import (
    router as fleet_router
)

from backend.api.routes.drift import (
    router as drift_router
)

from backend.api.routes.compliance import (
    router as compliance_router
)

from backend.api.routes.realtime import (
    router as realtime_router
)

from backend.api.routes.notifications import (
    router as notifications_router
)
from backend.api.routes.auth import (
    router as auth_router
)
from backend.database.init_db import (
    initialize_database
)

app = FastAPI(
    title="Docker AI Agent",
    version="1.0.0",
)

app.include_router(
    notifications_router,
    prefix="/notifications",
    tags=["Notifications"]
)

app.include_router(
    realtime_router,
    tags=["Realtime"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(

    fleet_router,

    prefix="/fleet",

    tags=["Fleet"]
)

app.include_router(
    compliance_router,
    prefix="/compliance",
    tags=["Compliance"]
)

app.include_router(
    drift_router,
    prefix="/drift",
    tags=["Drift"]
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    hosts_router,
    prefix="/hosts",
    tags=["Hosts"]
)

app.include_router(
    incidents_router,
    prefix="/incidents",
    tags=["Incidents"]
)

app.include_router(
    watcher_router,
    prefix="/watcher",
    tags=["Watcher"]
)

app.include_router(
    monitoring_router,
    prefix="/monitoring",
    tags=["Monitoring"]
)

app.include_router(
    findings_router,
    prefix="/findings",
    tags=["Findings"]
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

# Docker Agent Query API
app.include_router(
    docker_router,
    prefix="/docker-agent",
    tags=["Docker Agent"],
)


# System APIs
app.include_router(
    system_router,
    prefix="/system",
    tags=["System"],
)

# Tools APIs
app.include_router(
    tools_router,
    prefix="/tools",
    tags=["Tools"],
)

app.include_router(
    approval_router,
    prefix="/approval",
    tags=["Approval"]
)

app.include_router(
    audit_router,
    prefix="/audit",
    tags=["Audit"]
)

app.include_router(
    remediation_router,
    prefix="/remediation",
    tags=["Remediation"]
)

app.include_router(
    remediation_execute_router,
    prefix="/remediation/execute",
    tags=["Remediation Execute"]
)

@app.on_event("startup")
def startup_event():

    initialize_database()
    start_scheduler()

    print(
        "Docker Monitoring Scheduler Started"
    )

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }