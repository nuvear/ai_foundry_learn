# AI DevTeam — Deployment Engineer Agent
from agents.base_agent import BaseAgent


class DeploymentEngineerAgent(BaseAgent):
    """
    Produces Dockerfiles, CI/CD pipelines, environment configuration,
    and deployment instructions for the tested application build.
    """

    def __init__(self):
        super().__init__(
            name="Deployment Engineer",
            role="deploy",
            prompt_file="deployment_engineer.txt",
            temperature=0.3,   # Low temperature for precise infrastructure code
            max_tokens=4096,
        )
