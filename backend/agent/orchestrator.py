from langgraph.graph import (
    StateGraph,
    END,
)

from backend.agent.state import (
    AgentState
)

from backend.agent.planner import (
    planner
)

from backend.agent.approval import (
    approval_node
)

from backend.agent.executor import (
    executor
)

builder = StateGraph(
    AgentState
)

# Nodes
builder.add_node(
    "planner",
    planner
)

builder.add_node(
    "approval",
    approval_node
)

builder.add_node(
    "executor",
    executor
)

# Entry Point
builder.set_entry_point(
    "planner"
)

# Flow
builder.add_edge(
    "planner",
    "approval"
)

builder.add_edge(
    "approval",
    "executor"
)

builder.add_edge(
    "executor",
    END
)

graph = builder.compile()