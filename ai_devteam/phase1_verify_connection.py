"""
phase1_verify_connection.py
----------------------------
Phase 1 — Verification Script

Run this script after completing the Azure and local setup steps
in PHASE_1_SETUP.md. It will:

  1. Load your .env configuration
  2. Connect to your Microsoft AI Foundry project
  3. Send a single test message to your deployed model
  4. Print the response

If this script runs without errors, your Phase 1 setup is complete
and you are ready to move on to Phase 2.

Usage:
    python phase1_verify_connection.py
"""

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.inference.models import SystemMessage, UserMessage
from rich.console import Console
from rich.panel import Panel
from shared.config import load_config

console = Console()


def main():
    console.print(Panel.fit(
        "[bold cyan]AI DevTeam — Phase 1: Connection Verification[/bold cyan]",
        border_style="cyan"
    ))

    # Step 1: Load configuration from .env
    console.print("\n[yellow]Step 1:[/yellow] Loading configuration from .env ...")
    config = load_config()
    console.print(f"  [green]✓[/green] Connection string loaded")
    console.print(f"  [green]✓[/green] Model deployment: [bold]{config.model_deployment_name}[/bold]")

    # Step 2: Create the Foundry project client using keyless auth
    console.print("\n[yellow]Step 2:[/yellow] Connecting to Microsoft AI Foundry ...")
    client = AIProjectClient.from_connection_string(
        conn_str=config.connection_string,
        credential=DefaultAzureCredential(),
    )
    console.print("  [green]✓[/green] Connected to Foundry project")

    # Step 3: Get a chat completions client for our deployed model
    console.print("\n[yellow]Step 3:[/yellow] Sending test message to model ...")
    chat_client = client.inference.get_chat_completions_client()

    response = chat_client.complete(
        model=config.model_deployment_name,
        messages=[
            SystemMessage(content=(
                "You are the Project Manager of an AI-powered software development team "
                "called 'AI DevTeam'. Introduce yourself in one sentence."
            )),
            UserMessage(content="Who are you?"),
        ],
    )

    reply = response.choices[0].message.content
    console.print(f"  [green]✓[/green] Model responded successfully\n")

    # Step 4: Print the result
    console.print(Panel(
        f"[bold white]{reply}[/bold white]",
        title="[green]Model Response[/green]",
        border_style="green"
    ))

    console.print(Panel.fit(
        "[bold green]Phase 1 Complete![/bold green]\n"
        "Your Azure AI Foundry project is connected and the model is responding.\n"
        "You are ready to start [bold]Phase 2: Core Intelligence[/bold].",
        border_style="green"
    ))


if __name__ == "__main__":
    main()
