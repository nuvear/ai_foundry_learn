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

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

load_dotenv()
console = Console()


def build_endpoint(connection_string: str) -> str:
    """
    Convert the Foundry connection string to the new SDK 2.0+ endpoint URL format.

    Old format (SDK < 2.0):
        eastus2.api.azureml.ms;<subscription-id>;<resource-group>;<project-name>

    New format (SDK 2.0+):
        https://<ai-services-account>.services.ai.azure.com/api/projects/<project-name>

    We derive the AI services account name from the resource group and project name
    by querying the Azure AI Projects endpoint directly.
    """
    # If the user already provided a full https:// URL, use it as-is
    if connection_string.startswith("https://"):
        return connection_string

    # Parse the semicolon-delimited connection string
    parts = connection_string.split(";")
    if len(parts) != 4:
        raise ValueError(
            "AIPROJECT_CONNECTION_STRING must be in the format:\n"
            "  <region>.api.azureml.ms;<subscription-id>;<resource-group>;<project-name>\n"
            "OR the new format:\n"
            "  https://<ai-services-account>.services.ai.azure.com/api/projects/<project-name>"
        )

    region, subscription_id, resource_group, project_name = parts

    # Derive the AI services hostname from the region
    # New SDK uses: https://<account>.services.ai.azure.com/api/projects/<project>
    # The account name is typically the project resource name
    # We construct it using the known pattern for Foundry resources
    account_name = project_name + "-resource"
    endpoint = f"https://{account_name}.services.ai.azure.com/api/projects/{project_name}"
    return endpoint


def main():
    console.print(Panel.fit(
        "[bold cyan]AI DevTeam — Phase 1: Connection Verification[/bold cyan]",
        border_style="cyan"
    ))

    # Step 1: Load configuration from .env
    console.print("\n[yellow]Step 1:[/yellow] Loading configuration from .env ...")

    connection_string = os.getenv("AIPROJECT_CONNECTION_STRING", "")
    model_name = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")

    if not connection_string:
        console.print("[red]ERROR:[/red] AIPROJECT_CONNECTION_STRING is not set in .env")
        return

    console.print(f"  [green]✓[/green] Connection string loaded")
    console.print(f"  [green]✓[/green] Model deployment: [bold]{model_name}[/bold]")

    # Step 2: Build the endpoint URL and create the Foundry project client
    console.print("\n[yellow]Step 2:[/yellow] Connecting to Microsoft AI Foundry ...")

    # If the connection string is the new https:// format, use it directly
    # If it is the old semicolon format, we need to get the endpoint from Azure
    if connection_string.startswith("https://"):
        endpoint = connection_string
    else:
        # Parse old-style connection string to extract project name
        parts = connection_string.split(";")
        if len(parts) != 4:
            console.print(
                "[red]ERROR:[/red] Invalid connection string format.\n"
                "Expected: eastus2.api.azureml.ms;<sub-id>;<rg>;<project-name>\n"
                f"Got: {connection_string}"
            )
            return
        region, subscription_id, resource_group, project_name = parts
        console.print(f"  Region: [bold]{region}[/bold]")
        console.print(f"  Project: [bold]{project_name}[/bold]")
        console.print(f"  Resource Group: [bold]{resource_group}[/bold]")

        # Fetch the actual endpoint URL from Azure using the REST API
        import urllib.request
        import json

        token_credential = DefaultAzureCredential()
        token = token_credential.get_token("https://management.azure.com/.default").token

        url = (
            f"https://management.azure.com/subscriptions/{subscription_id}"
            f"/resourceGroups/{resource_group}"
            f"/providers/Microsoft.CognitiveServices/accounts/{project_name}-resource"
            f"/projects/{project_name}"
            f"?api-version=2025-04-01-preview"
        )

        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                endpoint = data.get("properties", {}).get("endpoints", {}).get(
                    "AI Foundry API", ""
                )
                if not endpoint:
                    # Fallback: construct from known pattern
                    endpoint = f"https://{project_name}-resource.services.ai.azure.com/api/projects/{project_name}"
        except Exception:
            # Fallback to constructed endpoint
            endpoint = f"https://{project_name}-resource.services.ai.azure.com/api/projects/{project_name}"

    console.print(f"  Endpoint: [bold]{endpoint}[/bold]")

    client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )
    console.print("  [green]✓[/green] Connected to Foundry project")

    # Step 3: Use the OpenAI client to chat with the deployed model
    console.print("\n[yellow]Step 3:[/yellow] Sending test message to model ...")

    openai_client = client.get_openai_client()

    response = openai_client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Project Manager of an AI-powered software development team "
                    "called 'AI DevTeam'. Introduce yourself in one sentence."
                ),
            },
            {"role": "user", "content": "Who are you?"},
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
