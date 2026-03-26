# AI DevTeam — Tester Agent
from agents.base_agent import BaseAgent


class TesterAgent(BaseAgent):
    """
    Validates the Developer's implementation against the FRD Acceptance Criteria
    and UX Specification. Produces a Test Report and Bug Reports.
    """

    def __init__(self):
        super().__init__(
            name="Tester",
            role="tester",
            prompt_file="tester.txt",
            temperature=0.3,   # Low temperature for consistent, structured test reports
            max_tokens=3000,
        )
