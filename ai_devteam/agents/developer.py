# AI DevTeam — Solution Developer Agent
# Two-tier model strategy: Developer uses a stronger model than the rest of the
# pipeline because it must produce complete, multi-file, runnable code while
# holding the full context of BA spec + UX spec + Arch doc + Tester feedback.
# Set DEVELOPER_MODEL_DEPLOYMENT_NAME in .env to override (e.g. gpt-4.1).
# Falls back to MODEL_DEPLOYMENT_NAME if not set.
from agents.base_agent import BaseAgent
from shared.config import config


class DeveloperAgent(BaseAgent):
    """
    Writes production-quality code, unit tests, and documentation
    based on the Architect's HLD and BA's User Stories.

    Uses DEVELOPER_MODEL_DEPLOYMENT_NAME from config (defaults to the
    pipeline-wide MODEL_DEPLOYMENT_NAME if not explicitly set).
    """

    def __init__(self):
        super().__init__(
            name="Solution Developer",
            role="developer",
            prompt_file="developer.txt",
            model_deployment=config.DEVELOPER_MODEL_DEPLOYMENT_NAME,
            temperature=0.2,   # Slightly lower than default for more deterministic code
            max_tokens=8192,   # Larger budget: multi-file output + Bug Fix Summary + Self-Validation
        )
