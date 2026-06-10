from rich.console import Console
from rich.panel import Panel

console = Console()


def show_banner():

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]Docker AI Agent[/bold cyan]",
            subtitle="Powered by Ollama + MCP"
        )
    )

    console.print()