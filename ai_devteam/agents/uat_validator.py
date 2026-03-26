# AI DevTeam — QA / UAT Validator Agent
from agents.base_agent import BaseAgent


class UATValidatorAgent(BaseAgent):
    """
    Performs final User Acceptance Testing by simulating the end user.
    Validates that the deployed application meets the original requirement.
    Provides final sign-off or rejection with actionable feedback.
    """

    def __init__(self):
        super().__init__(
            name="QA / UAT Validator",
            role="qa",
            prompt_file="uat_validator.txt",
            temperature=0.5,
            max_tokens=3000,
        )
