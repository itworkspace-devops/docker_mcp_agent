import json

from langchain_ollama import ChatOllama

from backend.config.settings import settings
from backend.agent.tool_router import route_query
from backend.agent.prompts import build_docker_agent_prompt


llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_url,
    temperature=0,
)


def planner(state):

    query = state["query"]
    history = state.get("history", [])

    # First try direct routing
    direct_tool = route_query(query)

    if direct_tool:

        return {

            "tool_name":
                direct_tool["tool_name"],

            "tool_args":
                direct_tool.get(
                    "tool_args",
                    {}
                ),

            "host_name":
                direct_tool.get(
                    "host_name"
                )
        }

    # Fallback to LLM

    # Format history for prompt
    history_str = ""
    for msg in history:
        history_str += f"{msg['role'].upper()}: {msg['content']}\n"

    prompt = build_docker_agent_prompt(query, history=history_str)

    result = llm.invoke(
        prompt
    )

    content = result.content.strip()

    print("=" * 80)
    print("LLM RESPONSE:")
    print(content)
    print("=" * 80)

    try:

        tool_data = json.loads(
            content
        )

        return {

            "tool_name":
                tool_data["tool_name"],

            "tool_args":
                tool_data.get(
                    "tool_args",
                    {}
                ),

            # LLM path currently does not parse hosts
            "host_name":
                tool_data.get(
                    "host_name"
                )
        }

    except Exception as ex:

        print(
            "Planner Error:",
            str(ex)
        )

        return {

            "error":
                str(ex),

            "tool_name":
                "",

            "tool_args":
                {},

            "host_name":
                None
        }