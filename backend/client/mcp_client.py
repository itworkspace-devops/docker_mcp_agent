import requests

from backend.config.settings import (
    settings
)

from backend.database.repository import (
    get_host_by_name
)


class MCPClient:

    def __init__(self):

        self.default_base_url = (

            f"http://{settings.mcp_host}:"
            f"{settings.mcp_port}"
        )

    def get_base_url(
        self,
        host_name=None
    ):
        return self.default_base_url

    def call(

        self,

        tool,

        arguments=None,

        host_name=None
    ):
        if arguments is None:
            arguments = {}
        
        if host_name:
            arguments["host_name"] = host_name

        payload = {

            "name":
                tool,

            "arguments":
                arguments
        }

        response = requests.post(

            f"{self.get_base_url()}/tools/call",

            json=payload,

            timeout=60
        )

        response.raise_for_status()

        return response.json()