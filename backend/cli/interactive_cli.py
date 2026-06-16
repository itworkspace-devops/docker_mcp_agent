from prompt_toolkit import prompt
from rich.console import Console
from rich.panel import Panel

from backend.agent.orchestrator import graph
from backend.client.mcp_client import MCPClient
from backend.cli.result_formatter import (
    format_result
)

console = Console()
mcp = MCPClient()


class DockerAgentCLI:

    def show_banner(self):

        console.print(
            Panel.fit(
                "[bold cyan]Docker AI Agent v1.0[/bold cyan]",
                title="Docker Agent",
            )
        )

        try:

            health = mcp.call(
                "docker_ping"
            )

            if health.get("success"):

                console.print(
                    "[green]✓ MCP Connected[/green]"
                )

            else:

                console.print(
                    "[red]✗ MCP Disconnected[/red]"
                )

        except Exception:

            console.print(
                "[red]✗ MCP Disconnected[/red]"
            )

    def run(self):

        self.show_banner()

        while True:

            try:

                query = prompt(
                    "\nDocker Agent > "
                )

                if not query:
                    continue

                if query.lower() in (
                    "exit",
                    "quit",
                ):
                    break

                if query.lower() == "clear":

                    console.clear()

                    self.show_banner()

                    continue

                if query.lower() == "health":

                    result = mcp.call(
                        "docker_ping"
                    )

                    console.print(result)

                    continue

                result = graph.invoke(
                    {
                        "query": query,
                        "origin": "cli"
                    }
                )

                formatted = format_result(
                    result["result"]
                )

                console.print(
                    "\n[green]Response[/green]"
                )

                console.print(
                    formatted
                )

            except KeyboardInterrupt:

                continue

            except Exception as ex:

                console.print(
                    f"[red]{str(ex)}[/red]"
                )