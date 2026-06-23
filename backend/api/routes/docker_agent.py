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

def _render_assistant_message(result):
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if result.get("message"):
            return result["message"]
        if result.get("success") is False:
            return result.get("error") or "Operation failed."
        data = result.get("data")
        if isinstance(data, str):
            return data
        if isinstance(data, list):
            return f"Returned {len(data)} item(s)."
        if isinstance(data, dict):
            if "tool_name" in data and "result" in data and isinstance(data["result"], (dict, list, str)):
                return "Completed multi-step request."
            parts = []
            for key in ("container", "image", "network", "volume", "action", "risk", "free_port"):
                if key in data and data[key] is not None:
                    parts.append(f"{key}={data[key]}")
            if parts:
                return " | ".join(parts)
            return "Operation completed."
    return str(result)

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
    for msg in history[-6:]:
        history_context.append({
            "role": msg.role,
            "content": msg.content[:500],
        })

    try:
        result = graph.invoke(
            {
                "query": request.query,
                "origin": "ui",
                "history": history_context,
                "host_name": request.host_name,
            }
        )
        
        # Save agent response
        response_content = _render_assistant_message(result["result"])
             
        save_chat_message(session_id, "agent", response_content)

    finally:
        clear_current_user()

    return QueryResponse(
        success=True,
        response=result["result"],
    )
