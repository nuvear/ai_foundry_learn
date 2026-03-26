"""
shared/config.py
----------------
Central configuration loader for AI DevTeam.
Reads all required environment variables from .env and exposes
them as a typed Config object used by every agent.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the ai_devteam directory
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


class Config:
    """Typed configuration for the AI DevTeam project."""

    def __init__(self):
        required = {
            "AIPROJECT_CONNECTION_STRING": "Your Foundry project endpoint URL (https://...)",
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
                "Copy ai_devteam/.env.example to ai_devteam/.env and fill in your values.\n"
                "Then run: az login"
            )

        # Microsoft AI Foundry project endpoint URL
        self.AIPROJECT_CONNECTION_STRING: str = os.environ["AIPROJECT_CONNECTION_STRING"]

        # Name of the deployed model in Foundry (e.g. "gpt-4o")
        self.MODEL_DEPLOYMENT_NAME: str = os.environ["MODEL_DEPLOYMENT_NAME"]

        # Optional stronger model for the Developer agent (e.g. "gpt-4.1").
        # Falls back to MODEL_DEPLOYMENT_NAME if not set in .env.
        self.DEVELOPER_MODEL_DEPLOYMENT_NAME: str = (
            os.getenv("DEVELOPER_MODEL_DEPLOYMENT_NAME") or self.MODEL_DEPLOYMENT_NAME
        )

        # Azure subscription details (used by Deployment Engineer agent)
        self.AZURE_SUBSCRIPTION_ID: str = os.environ["AZURE_SUBSCRIPTION_ID"]
        self.AZURE_RESOURCE_GROUP: str = os.environ["AZURE_RESOURCE_GROUP"]

        # Directory where agent outputs are saved
        self.OUTPUTS_DIR: str = str(
            Path(__file__).parent.parent / "outputs"
        )

    def __repr__(self) -> str:
        return (
            f"Config("
            f"endpoint={self.AIPROJECT_CONNECTION_STRING[:40]}..., "
            f"model={self.MODEL_DEPLOYMENT_NAME}, "
            f"developer_model={self.DEVELOPER_MODEL_DEPLOYMENT_NAME}, "
            f"subscription={self.AZURE_SUBSCRIPTION_ID[:8]}...)"
        )


# Singleton — import this everywhere: from shared.config import config
config = Config()
