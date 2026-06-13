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

        if not host_name:

            return self.default_base_url

        host = get_host_by_name(
            host_name
        )

        if not host:

            raise Exception(
                f"Host not found: {host_name}"
            )

        return (

            f"http://{host.host}:"
            f"{host.port}"
        )

    def call(

        self,

        tool,

        arguments=None,

        host_name=None
    ):

        payload = {

            "name":
                tool,

            "arguments":
                arguments or {}
        }

        response = requests.post(

            f"{self.get_base_url(host_name)}/tools/call",

            json=payload,

            timeout=60
        )

        response.raise_for_status()

        return response.json()