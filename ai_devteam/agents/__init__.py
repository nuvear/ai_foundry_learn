# AI DevTeam — Agent Package
# Import all agents here for clean access: from agents import DeveloperAgent

from agents.base_agent import BaseAgent, AgentResponse
from agents.project_manager import ProjectManagerAgent
from agents.business_analyst import BusinessAnalystAgent
from agents.ux_designer import UXDesignerAgent
from agents.architect import ArchitectAgent
from agents.developer import DeveloperAgent
from agents.tester import TesterAgent
from agents.deployment_engineer import DeploymentEngineerAgent
from agents.uat_validator import UATValidatorAgent

__all__ = [
    "BaseAgent",
    "AgentResponse",
    "ProjectManagerAgent",
    "BusinessAnalystAgent",
    "UXDesignerAgent",
    "ArchitectAgent",
    "DeveloperAgent",
    "TesterAgent",
    "DeploymentEngineerAgent",
    "UATValidatorAgent",
]

# Registry: maps CLI --agent names to agent classes
AGENT_REGISTRY = {
    "pm": ProjectManagerAgent,
    "ba": BusinessAnalystAgent,
    "ux": UXDesignerAgent,
    "architect": ArchitectAgent,
    "developer": DeveloperAgent,
    "tester": TesterAgent,
    "deploy": DeploymentEngineerAgent,
    "qa": UATValidatorAgent,
}
