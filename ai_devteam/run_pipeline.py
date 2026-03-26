#!/usr/bin/env python3
"""
AI DevTeam — Phase 3: Pipeline Runner
========================================
Chains all 8 agents in sequence, passing each agent's output as
context to the next. All outputs are saved to a timestamped workspace.

Usage:
    python run_pipeline.py --requirement "Build a todo list REST API"
    python run_pipeline.py --requirement "Build a todo list REST API" --start-from architect
    python run_pipeline.py --workspace workspaces/todo_list_20240101_120000 --start-from tester

Design: Azure Blueprint / Technical Documentation Elevated
"""

import argparse
import sys
import time
from pathlib import Path

# Ensure the ai_devteam package root is on the path
sys.path.insert(0, str(Path(__file__).parent))

from agents import (
    ProjectManagerAgent,
    BusinessAnalystAgent,
    UXDesignerAgent,
    ArchitectAgent,
    DeveloperAgent,
    TesterAgent,
    DeploymentEngineerAgent,
    UATValidatorAgent,
)
from tools.workspace import Workspace


# ── Pipeline definition ───────────────────────────────────────────────────────
# Each step defines: agent class, CLI shortname, and how to build its input
# from the workspace (what prior outputs to include as context).

PIPELINE = [
    {
        "key":   "project_manager",
        "label": "Project Manager",
        "agent": ProjectManagerAgent,
        "context_agents": [],   # First agent — only gets the raw requirement
    },
    {
        "key":   "business_analyst",
        "label": "Business Analyst",
        "agent": BusinessAnalystAgent,
        "context_agents": ["project_manager"],
    },
    {
        "key":   "ux_designer",
        "label": "UI/UX Designer",
        "agent": UXDesignerAgent,
        "context_agents": ["project_manager", "business_analyst"],
    },
    {
        "key":   "architect",
        "label": "Architect",
        "agent": ArchitectAgent,
        "context_agents": ["project_manager", "business_analyst", "ux_designer"],
    },
    {
        "key":   "developer",
        "label": "Solution Developer",
        "agent": DeveloperAgent,
        "context_agents": ["business_analyst", "ux_designer", "architect"],
    },
    {
        "key":   "tester",
        "label": "Tester",
        "agent": TesterAgent,
        "context_agents": ["business_analyst", "architect", "developer"],
    },
    {
        "key":   "deployment_engineer",
        "label": "Deployment Engineer",
        "agent": DeploymentEngineerAgent,
        "context_agents": ["architect", "developer"],
    },
    {
        "key":   "uat_validator",
        "label": "QA / UAT Validator",
        "agent": UATValidatorAgent,
        "context_agents": ["business_analyst", "developer", "tester"],
    },
]

AGENT_KEYS = [step["key"] for step in PIPELINE]


# ── Helpers ───────────────────────────────────────────────────────────────────

def build_agent_input(requirement: str, workspace: Workspace, context_agents: list) -> str:
    """
    Build the input message for an agent by combining the original requirement
    with the outputs of prior agents listed in context_agents.
    """
    parts = [f"## Original Requirement\n{requirement}"]

    for agent_key in context_agents:
        prior_output = workspace.read_agent_output(agent_key)
        if prior_output:
            label = next(
                (s["label"] for s in PIPELINE if s["key"] == agent_key),
                agent_key.replace("_", " ").title()
            )
            parts.append(f"## {label} Output\n{prior_output}")

    return "\n\n---\n\n".join(parts)


def print_banner(text: str, width: int = 62) -> None:
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def print_agent_header(step_num: int, total: int, label: str) -> None:
    print(f"\n{'─' * 62}")
    print(f"  Step {step_num}/{total}  |  {label}")
    print(f"{'─' * 62}")


def print_agent_result(response, saved_path) -> None:
    preview = response.content[:400].replace("\n", " ")
    if len(response.content) > 400:
        preview += "..."
    print(f"\n  ✅ {response.agent_name} completed in {response.duration_seconds:.1f}s")
    print(f"  📁 Saved → {saved_path}")
    print(f"\n  Preview:\n  {preview}\n")


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(requirement: str, start_from: str = "project_manager",
                 workspace: Workspace = None) -> Workspace:
    """
    Run the full agent pipeline for a given requirement.

    Args:
        requirement:  The user's natural language requirement.
        start_from:   Agent key to start from (skip earlier agents).
        workspace:    An existing Workspace to resume; creates a new one if None.

    Returns:
        The Workspace object with all outputs.
    """
    if workspace is None:
        workspace = Workspace.create(requirement)

    print_banner(f"AI DevTeam Pipeline  |  Phase 3")
    print(f"\n  Requirement : {requirement[:80]}")
    print(f"  Workspace   : {workspace.path}")
    print(f"  Starting at : {start_from}")

    # Determine which steps to run
    start_idx = next(
        (i for i, s in enumerate(PIPELINE) if s["key"] == start_from), 0
    )
    steps_to_run = PIPELINE[start_idx:]
    total = len(PIPELINE)

    for step in steps_to_run:
        step_num = AGENT_KEYS.index(step["key"]) + 1
        print_agent_header(step_num, total, step["label"])

        # Build input from requirement + prior agent outputs
        agent_input = build_agent_input(requirement, workspace, step["context_agents"])

        # Instantiate and run the agent
        agent = step["agent"]()
        workspace.log(f"Running {step['label']}...")

        response = agent.run(agent_input, clear_history=True)

        # Save to workspace
        saved_path = workspace.save_agent_output(step["key"], response.content)
        print_agent_result(response, saved_path)

        # Small pause to avoid rate limiting
        time.sleep(1)

    workspace.print_summary()
    return workspace


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI DevTeam — Phase 3 Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the full pipeline from scratch
  python run_pipeline.py --requirement "Build a todo list REST API with FastAPI"

  # Start from a specific agent (skip earlier ones)
  python run_pipeline.py --requirement "Build a todo list REST API" --start-from architect

  # Resume an existing workspace from the tester step
  python run_pipeline.py --workspace workspaces/todo_list_20240101_120000 --start-from tester

Available agent keys:
  project_manager, business_analyst, ux_designer, architect,
  developer, tester, deployment_engineer, uat_validator
        """
    )
    parser.add_argument(
        "--requirement", "-r",
        type=str,
        help="The user requirement to build (natural language)"
    )
    parser.add_argument(
        "--start-from", "-s",
        type=str,
        default="project_manager",
        choices=AGENT_KEYS,
        metavar="AGENT_KEY",
        help=f"Start the pipeline from this agent. Choices: {', '.join(AGENT_KEYS)}"
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        default=None,
        help="Path to an existing workspace to resume"
    )

    args = parser.parse_args()

    # Validate: need either a requirement or an existing workspace
    if not args.requirement and not args.workspace:
        parser.error("Provide --requirement to start a new pipeline, or --workspace to resume.")

    # Load or derive requirement
    if args.workspace:
        ws = Workspace.load(args.workspace)
        req_file = ws.path / "requirement.txt"
        if req_file.exists():
            requirement = req_file.read_text(encoding="utf-8").strip()
        elif args.requirement:
            requirement = args.requirement
        else:
            parser.error("--workspace provided but requirement.txt not found. Also pass --requirement.")
    else:
        requirement = args.requirement
        ws = None

    run_pipeline(
        requirement=requirement,
        start_from=args.start_from,
        workspace=ws,
    )


if __name__ == "__main__":
    main()
