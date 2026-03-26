# AI DevTeam — Solution Developer Agent
from agents.base_agent import BaseAgent


class DeveloperAgent(BaseAgent):
    """
    Writes production-quality code, unit tests, and documentation
    based on the Architect's HLD and BA's User Stories.
    """

    def __init__(self):
        super().__init__(
            name="Solution Developer",
            role="developer",
            prompt_file="developer.txt",
            temperature=0.3,   # Low temperature for deterministic, correct code
            max_tokens=4096,
        )
