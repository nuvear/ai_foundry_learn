# AI DevTeam — UI/UX Designer Agent
from agents.base_agent import BaseAgent


class UXDesignerAgent(BaseAgent):
    """
    Translates User Stories into wireframes, user flows, component specifications,
    and a design system. Ensures the Developer builds the right interface.
    """

    def __init__(self):
        super().__init__(
            name="UI/UX Designer",
            role="ux",
            prompt_file="ux_designer.txt",
            temperature=0.7,   # Slightly higher for creative design decisions
            max_tokens=3000,
        )
