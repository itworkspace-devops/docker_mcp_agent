import json

from langchain_ollama import ChatOllama

from backend.config.settings import settings


llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_url,
    temperature=0,
)


def planner(state):

    query = state["query"]

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

    result = llm.invoke(prompt)

    content = result.content.strip()

    print("LLM RESPONSE:", content)

    return {
        "tool_name": content
    }