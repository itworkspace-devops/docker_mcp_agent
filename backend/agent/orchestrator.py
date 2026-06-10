from langgraph.graph import StateGraph

from .planner import planner
from .executor import executor
from .state import AgentState


builder = StateGraph(AgentState)

builder.add_node(
    "planner",
    planner
)

builder.add_node(
    "executor",
    executor
)

builder.set_entry_point(
    "planner"
)

builder.add_edge(
    "planner",
    "executor"
)

builder.set_finish_point(
    "executor"
)

graph = builder.compile()