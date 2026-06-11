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

app = FastAPI(
    title="Docker AI Agent",
    version="1.0.0",
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


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }