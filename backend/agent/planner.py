import json

from langchain_ollama import ChatOllama

from backend.config.settings import settings
from backend.agent.tool_router import route_query


llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_url,
    temperature=0,
)


def planner(state):

    query = state["query"]

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

    prompt = f"""
You are a Docker AI Agent.

Return ONLY valid JSON.

Available tools:

docker_ps
docker_images
docker_inspect
docker_logs
docker_restart
docker_start
docker_stop
docker_pull
docker_info
docker_ping
docker_version
incident_investigate

User request:

{query}

Return EXACTLY:

{{
    "tool_name": "docker_ps",
    "tool_args": {{}}
}}

No explanation.
No markdown.
Only JSON.
"""

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