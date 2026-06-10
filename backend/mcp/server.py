from fastapi import FastAPI
from fastapi import HTTPException

from .schemas import ToolRequest
from .registry import TOOL_REGISTRY

app = FastAPI()

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/tools/call")
def call_tool(req: ToolRequest):

    tool = TOOL_REGISTRY.get(req.name)

    if not tool:

        raise HTTPException(
            404,
            f"Unknown tool {req.name}"
        )

    return tool(req.arguments)