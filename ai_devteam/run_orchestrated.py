#!/usr/bin/env python3
"""
AI DevTeam — Phase 4: Orchestrated Pipeline Runner
====================================================
Uses the OrchestratorPM to run the full agent pipeline with:
  - Active feedback loops (Tester → Developer)
  - Quality gates (PM verifies bug acknowledgement)
  - Retry logic with configurable max retries
  - pipeline_state.json written after every decision

Usage:
    python run_orchestrated.py --requirement "Build a todo list REST API"
    python run_orchestrated.py --requirement "Build a todo list REST API" --max-retries 5
    python run_orchestrated.py --workspace workspaces/todo_list_20240101_120000

Design: Azure Blueprint / Technical Documentation Elevated
"""

import argparse
import sys
from pathlib import Path

# Ensure the ai_devteam package root is on the path
sys.path.insert(0, str(Path(__file__).parent))

from agents.orchestrator_pm import OrchestratorPM
from tools.workspace import Workspace


def main():
    parser = argparse.ArgumentParser(
        description="AI DevTeam — Phase 4 Orchestrated Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the full orchestrated pipeline from scratch
  python run_orchestrated.py --requirement "Build a todo list REST API with FastAPI"

  # Allow more feedback loops between Tester and Developer
  python run_orchestrated.py --requirement "Build a todo list REST API" --max-retries 5

  # Resume an existing workspace (re-runs from business_analyst)
  python run_orchestrated.py --workspace workspaces/todo_list_20240101_120000

Available agent keys (for reference):
  project_manager, business_analyst, ux_designer, architect,
  developer, tester, deployment_engineer, uat_validator
        """
    )
    parser.add_argument(
        "--requirement", "-r",
        type=str,
        default=None,
        help="The user requirement to build (natural language)"
    )
    parser.add_argument(
        "--max-retries", "-m",
        type=int,
        default=3,
        help="Maximum number of retries per agent (default: 3)"
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
    ws = None
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

    # Run the orchestrated pipeline
    pm = OrchestratorPM(max_retries=args.max_retries)
    pm.orchestrate(requirement=requirement, workspace=ws)


if __name__ == "__main__":
    main()
