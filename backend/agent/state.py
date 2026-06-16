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

    result: Dict[str, Any]

    error: Optional[str]

    approval_required: bool

    approved: bool

    execution_id: str
    
    origin: str