from langchain_ollama import ChatOllama

from backend.config.settings import (
    settings
)

llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_url,
    temperature=0,
)


def analyze_incident(
    diagnostics
):

    logs = str(
        diagnostics.get(
            "logs",
            {}
        )
    )

    inspect_data = str(
        diagnostics.get(
            "inspect",
            {}
        )
    )

    prompt = f"""
You are a Docker SRE.

Analyze:

LOGS:
{logs[:4000]}

INSPECT:
{inspect_data[:2000]}

Return ONLY:

Root Cause:
Severity:
Recommendation:
"""

    response = llm.invoke(
        prompt
    )

    return {

        "analysis":
            response.content
    }