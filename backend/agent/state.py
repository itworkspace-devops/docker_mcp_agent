from typing import TypedDict


class AgentState(TypedDict):

    query: str

    intent: str

    tool_name: str

    tool_args: dict

    result: str