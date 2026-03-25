"""
shared/config.py
----------------
Central configuration loader for AI DevTeam.
Reads all required environment variables from .env and exposes
them as a typed Config object used by every agent.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file from the project root (ai_devteam directory)
load_dotenv()


@dataclass
class Config:
    """Typed configuration for the AI DevTeam project."""

    # Microsoft AI Foundry project connection string
    connection_string: str

    # Name of the deployed model in Foundry (e.g. "gpt-4o")
    model_deployment_name: str

    # Azure subscription details (used by Deployment Engineer agent)
    azure_subscription_id: str
    azure_resource_group: str


def load_config() -> Config:
    """
    Load and validate all required environment variables.
    Raises a clear error if any required variable is missing.
    """
    required = {
        "AIPROJECT_CONNECTION_STRING": "Your Foundry project connection string",
        "MODEL_DEPLOYMENT_NAME": "The name of your deployed model (e.g. gpt-4o)",
        "AZURE_SUBSCRIPTION_ID": "Your Azure subscription ID",
        "AZURE_RESOURCE_GROUP": "Your Azure resource group name",
    }

    missing = [key for key in required if not os.getenv(key)]
    if missing:
        lines = "\n".join(
            f"  - {key}: {required[key]}" for key in missing
        )
        raise EnvironmentError(
            f"\n\nMissing required environment variables:\n{lines}\n\n"
            "Copy ai_devteam/.env.example to ai_devteam/.env and fill in your values."
        )

    return Config(
        connection_string=os.environ["AIPROJECT_CONNECTION_STRING"],
        model_deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
        azure_subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
        azure_resource_group=os.environ["AZURE_RESOURCE_GROUP"],
    )
