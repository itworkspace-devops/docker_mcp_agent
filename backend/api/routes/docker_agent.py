from fastapi import APIRouter, Depends

from backend.agent.orchestrator import graph
from backend.api.schemas.query import (
    QueryRequest,
    QueryResponse,
)
from backend.security.auth import (
    get_current_user,
    set_current_user,
    clear_current_user,
)

router = APIRouter()


def authorize_request(current_user = Depends(get_current_user)):

    set_current_user(current_user)
    return current_user


@router.post(
    "/query",
    response_model=QueryResponse,
)
def docker_query(
    request: QueryRequest,
    current_user=Depends(authorize_request),
):

    try:
        result = graph.invoke(
            {
                "query": request.query,
                "origin": "ui"
            }
        )
    finally:
        clear_current_user()

    return QueryResponse(
        success=True,
        response=result["result"],
    )