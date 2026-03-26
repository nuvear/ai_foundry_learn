# =============================================================================
# AI DevTeam — Base Agent Class
# =============================================================================
# Design: Azure Blueprint / Technical Documentation Elevated
# All agents inherit from BaseAgent. It handles:
#   - Connection to Microsoft AI Foundry via AIProjectClient
#   - Loading the system prompt for the agent's role
#   - Sending a user message and returning a structured response
#   - Conversation history (multi-turn support)
#   - Logging each interaction to the outputs/ directory
# =============================================================================

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

from shared.config import config


class AgentResponse:
    """Structured response returned by every agent."""

    def __init__(
        self,
        agent_name: str,
        role: str,
        content: str,
        input_message: str,
        duration_seconds: float,
    ):
        self.agent_name = agent_name
        self.role = role
        self.content = content
        self.input_message = input_message
        self.duration_seconds = duration_seconds
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        return {
            "agent": self.agent_name,
            "role": self.role,
            "timestamp": self.timestamp,
            "duration_seconds": round(self.duration_seconds, 2),
            "input": self.input_message,
            "output": self.content,
        }

    def __str__(self) -> str:
        return self.content


class BaseAgent:
    """
    Base class for all AI DevTeam agents.

    Usage:
        class DeveloperAgent(BaseAgent):
            def __init__(self):
                super().__init__(
                    name="Solution Developer",
                    role="developer",
                    prompt_file="developer.txt",
                )

    The agent automatically:
    - Loads its system prompt from prompts/<prompt_file>
    - Connects to Foundry using DefaultAzureCredential (keyless auth)
    - Maintains conversation history for multi-turn interactions
    - Saves all outputs to outputs/<role>/<timestamp>.json
    """

    def __init__(
        self,
        name: str,
        role: str,
        prompt_file: str,
        model_deployment: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        self.name = name
        self.role = role
        self.model_deployment = model_deployment or config.MODEL_DEPLOYMENT_NAME
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Load system prompt
        self.system_prompt = self._load_prompt(prompt_file)

        # Conversation history (list of message dicts for multi-turn)
        self._history: List[Dict] = []

        # Lazy-initialised clients
        self._client: Optional[AIProjectClient] = None
        self._openai_client = None

        # Ensure output directory exists
        self._output_dir = Path(config.OUTPUTS_DIR) / role
        self._output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, user_input: str, clear_history: bool = False) -> AgentResponse:
        """
        Send a message to this agent and get a structured response.

        Args:
            user_input:    The message or task to send to the agent.
            clear_history: If True, starts a fresh conversation (no memory
                           of previous turns). Default is False.

        Returns:
            AgentResponse with the agent's reply and metadata.
        """
        if clear_history:
            self._history = []

        start = datetime.utcnow()

        # Build the messages list: system prompt + history + new user message
        messages = self._build_messages(user_input)

        # Call the model
        raw_content = self._call_model(messages)

        duration = (datetime.utcnow() - start).total_seconds()

        # Append to history for multi-turn support
        self._history.append({"role": "user", "content": user_input})
        self._history.append({"role": "assistant", "content": raw_content})

        response = AgentResponse(
            agent_name=self.name,
            role=self.role,
            content=raw_content,
            input_message=user_input,
            duration_seconds=duration,
        )

        # Persist the interaction to disk
        self._save_output(response)

        return response

    def clear_history(self) -> None:
        """Reset conversation history."""
        self._history = []

    @property
    def history(self) -> List[Dict]:
        """Return a copy of the conversation history."""
        return list(self._history)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_client(self) -> AIProjectClient:
        """Lazily initialise and return the Foundry project client."""
        if self._client is None:
            credential = AzureCliCredential()
            self._client = AIProjectClient(
                endpoint=config.AIPROJECT_CONNECTION_STRING,
                credential=credential,
            )
        return self._client

    def _get_openai_client(self):
        """Lazily initialise and return the OpenAI-compatible client via Foundry."""
        if self._openai_client is None:
            self._openai_client = self._get_client().get_openai_client()
        return self._openai_client

    def _load_prompt(self, prompt_file: str) -> str:
        """Load the system prompt from the prompts directory."""
        prompt_path = Path(__file__).parent.parent / "prompts" / prompt_file
        if not prompt_path.exists():
            raise FileNotFoundError(
                f"System prompt not found: {prompt_path}\n"
                f"Make sure '{prompt_file}' exists in the prompts/ directory."
            )
        return prompt_path.read_text(encoding="utf-8").strip()

    def _build_messages(self, user_input: str) -> List:
        """Construct the full message list for the API call."""
        messages = [{"role": "system", "content": self.system_prompt}]

        # Replay conversation history
        for msg in self._history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the new user message
        messages.append({"role": "user", "content": user_input})
        return messages

    def _call_model(self, messages: List) -> str:
        """Send messages to the deployed model and return the text response."""
        openai_client = self._get_openai_client()

        response = openai_client.chat.completions.create(
            model=self.model_deployment,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    def _save_output(self, response: AgentResponse) -> None:
        """Save the agent interaction to a JSON file in outputs/."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = self._output_dir / f"{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(response.to_dict(), f, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}' model='{self.model_deployment}'>"
