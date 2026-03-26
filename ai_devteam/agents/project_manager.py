# AI DevTeam — Project Manager Agent
from agents.base_agent import BaseAgent


class ProjectManagerAgent(BaseAgent):
    """
    The Orchestrator of the AI DevTeam pipeline.
    Receives raw user requirements and produces a structured Project Charter.
    Routes work to all other agents and tracks progress.
    """

    def __init__(self):
        super().__init__(
            name="Project Manager",
            role="pm",
            prompt_file="project_manager.txt",
            temperature=0.5,   # Lower temperature for structured, consistent output
            max_tokens=2048,
        )
