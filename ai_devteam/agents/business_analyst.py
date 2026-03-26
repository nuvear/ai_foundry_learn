# AI DevTeam — Business Analyst Agent
from agents.base_agent import BaseAgent


class BusinessAnalystAgent(BaseAgent):
    """
    Translates raw requirements into a Functional Requirements Document (FRD),
    User Stories, and Acceptance Criteria.
    """

    def __init__(self):
        super().__init__(
            name="Business Analyst",
            role="ba",
            prompt_file="business_analyst.txt",
            temperature=0.5,
            max_tokens=3000,
        )
