from typing import Any, Dict, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):

    query: str

    intent: str

    tool_name: str
    
    role: str
    
    host_name: str | None
    
    host: str

    tool_args: Dict[str, Any]

    tool_plan: list[dict[str, Any]]

    plan_index: int

    result: Dict[str, Any]

    error: Optional[str]

    approval_required: bool

    approved: bool

    execution_id: str
    
    origin: str
    
    history: list[dict[str, str]]
