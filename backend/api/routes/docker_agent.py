from fastapi import APIRouter

from backend.agent.orchestrator import graph

from backend.api.schemas.query import (
    QueryRequest,
    QueryResponse,
)

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
)
def docker_query(
    request: QueryRequest
):

    result = graph.invoke(
        {
            "query": request.query
        }
    )

    return QueryResponse(
        success=True,
        response=result["result"],
    )