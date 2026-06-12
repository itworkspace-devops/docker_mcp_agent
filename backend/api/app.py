from fastapi import FastAPI

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

app = FastAPI(
    title="Docker AI Agent",
    version="1.0.0",
)

app.include_router(
    watcher_router,
    prefix="/watcher",
    tags=["Watcher"]
)

app.include_router(
    findings_router,
    prefix="/findings",
    tags=["Findings"]
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

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }