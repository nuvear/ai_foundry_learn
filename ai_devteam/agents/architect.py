# AI DevTeam — Architect Agent
from agents.base_agent import BaseAgent


class ArchitectAgent(BaseAgent):
    """
    Designs the technical solution: technology stack, system architecture,
    data models, and API contracts based on the FRD and UX Specification.
    """

    def __init__(self):
        super().__init__(
            name="Architect",
            role="architect",
            prompt_file="architect.txt",
            temperature=0.4,   # Low temperature for precise technical decisions
            max_tokens=4096,
        )
