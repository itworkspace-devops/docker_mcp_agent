import json

from langchain_ollama import ChatOllama

from backend.config.settings import settings
from backend.agent.tool_router import route_query
from backend.agent.prompts import (
    build_docker_agent_prompt,
    build_plan_validation_prompt,
)


llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_url,
    temperature=0,
)


def planner(state):

    query = state["query"]
    history = state.get("history", [])
    selected_host = state.get("host_name")

    def with_host(tool_args=None):
        tool_args = tool_args or {}
        if selected_host and "host_name" not in tool_args:
            tool_args = {**tool_args, "host_name": selected_host}
        return tool_args

    def normalize_plan(tool_plan):
        normalized = []
        for step in tool_plan:
            if not isinstance(step, dict) or "tool_name" not in step:
                continue
            normalized.append({
                "tool_name": step["tool_name"],
                "tool_args": with_host(step.get("tool_args", {})),
            })
        return normalized

    def validate_plan(tool_plan):
        if not tool_plan:
            return tool_plan

        validation_prompt = build_plan_validation_prompt(
            query,
            json.dumps(tool_plan, indent=2),
        )

        validation_result = llm.invoke(validation_prompt)
        validation_content = validation_result.content.strip()

        print("=" * 80)
        print("PLAN VALIDATION RESPONSE:")
        print(validation_content)
        print("=" * 80)

        try:
            validation_data = json.loads(validation_content)
            if isinstance(validation_data, dict) and isinstance(validation_data.get("tool_plan"), list):
                return normalize_plan(validation_data["tool_plan"])
        except Exception as ex:
            print("Plan validation parse error:", str(ex))

        return tool_plan

    # First try direct routing
    direct_tool = route_query(query)

    if direct_tool:

        return {
            "tool_plan": [],

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
                ) or selected_host
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

        if "tool_plan" in tool_data and isinstance(tool_data["tool_plan"], list):
            tool_plan = normalize_plan(tool_data["tool_plan"])
            tool_plan = validate_plan(tool_plan)
            return {
                "tool_plan": tool_plan,
                "tool_name": tool_plan[0]["tool_name"] if tool_plan else "",
                "tool_args": tool_plan[0].get("tool_args", {}) if tool_plan else {},
                "host_name": tool_data.get("host_name") or selected_host,
            }

        return {
            "tool_plan": [],

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
                ) or selected_host
        }

    except Exception as ex:

        print(
            "Planner Error:",
            str(ex)
        )

        return {

            "error":
                str(ex),

            "tool_plan": [],

            "tool_name":
                "",

            "tool_args":
                {},

            "host_name":
                None
        }
