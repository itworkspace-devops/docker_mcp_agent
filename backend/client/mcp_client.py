import requests
from backend.config.settings import settings


class MCPClient:

    def __init__(self):

        self.base_url = (
            f"http://{settings.mcp_host}:"
            f"{settings.mcp_port}"
        )

    def call(
        self,
        tool,
        arguments=None
    ):

        payload = {
            "name": tool,
            "arguments": arguments or {}
        }

        response = requests.post(
            f"{self.base_url}/tools/call",
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()