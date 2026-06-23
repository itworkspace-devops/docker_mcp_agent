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


from backend.database.repository import (
    get_chat_messages,
    save_chat_message,
)

# ...

@router.post(
    "/query",
    response_model=QueryResponse,
)
def docker_query(
    request: QueryRequest,
    current_user=Depends(authorize_request),
):

    session_id = request.session_id or "default"
    
    # Save user message
    save_chat_message(session_id, "user", request.query)

    # Load history for context
    history = get_chat_messages(session_id)
    history_context = []
    for msg in history[-10:]: # last 10 messages
        history_context.append({"role": msg.role, "content": msg.content})

    try:
        result = graph.invoke(
            {
                "query": request.query,
                "origin": "ui",
                "history": history_context
            }
        )
        
        # Save agent response
        response_content = str(result["result"])
        if isinstance(result["result"], dict) and "message" in result["result"]:
             response_content = result["result"]["message"]
             
        save_chat_message(session_id, "agent", response_content)

    finally:
        clear_current_user()

    return QueryResponse(
        success=True,
        response=result["result"],
    )