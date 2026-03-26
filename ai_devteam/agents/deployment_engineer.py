"""
AI DevTeam — Deployment Engineer Agent
========================================
Produces Dockerfiles, CI/CD pipelines, environment configuration, and
deployment instructions for the tested application build.

Phase 4 upgrade: after writing the documentation, this agent also:
  1. Extracts all source files from the Developer's output into a runnable
     app/ directory inside the workspace.
  2. Installs Python dependencies via pip.
  3. Starts a local uvicorn server as a background process.
  4. Returns the live URL so the UAT Validator can test against a real server.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from agents.base_agent import BaseAgent
from tools.code_extractor import extract_files
from tools.local_deployer import LocalDeployer


class DeploymentEngineerAgent(BaseAgent):
    """
    Produces deployment artefacts and starts a local uvicorn server.
    """

    def __init__(self):
        super().__init__(
            name="Deployment Engineer",
            role="deploy",
            prompt_file="deployment_engineer.txt",
            temperature=0.3,
            max_tokens=4096,
        )
        self._deployer: LocalDeployer | None = None
        self.live_url: str | None = None

    # ── Post-run hook ──────────────────────────────────────────────────────────

    def deploy_local(self, workspace, developer_output: str = "") -> dict:
        """
        Called by the orchestrator after this agent's LLM response is saved.

        1. Extracts all source files from the Deployment Engineer's OWN output
           (which contains the full, final application code) into
           `workspace.path / "06_deployment" / "app"`.
        2. Falls back to the Developer's output if the DE output has no files.
        3. Installs dependencies.
        4. Starts uvicorn.
        5. Returns a result dict with keys: success, url, pid, error.
        """
        deploy_dir = workspace.path / "06_deployment" / "app"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        # ── Step 1: Extract source files from DE's own output first ────────────
        self.log("Extracting source files from Deployment Engineer output...")
        de_output = workspace.read_agent_output("deployment_engineer") or ""
        written = extract_files(de_output, deploy_dir)

        # Fall back to Developer output if DE produced no extractable files
        if not written and developer_output:
            self.log("  No files in DE output — falling back to Developer output...")
            written = extract_files(developer_output, deploy_dir)

        if not written:
            msg = (
                "Code extractor found no files in the Developer output. "
                "The server cannot be started without source files."
            )
            self.log(f"⚠️  {msg}")
            return {"success": False, "url": None, "pid": None, "error": msg}

        self.log(f"  Extracted {len(written)} file(s):")
        for f in written:
            self.log(f"    → {f.relative_to(workspace.path)}")

        # ── Step 2 & 3: Install deps and start server ─────────────────────────
        self.log("Starting local server on port 8000...")
        self._deployer = LocalDeployer(project_dir=deploy_dir, port=8000)
        result = self._deployer.deploy()

        if result["success"]:
            self.live_url = result["url"]
            self.log(f"✅ Server is live at {self.live_url}  (PID {result['pid']})")
        else:
            self.log(f"⚠️  Server failed to start: {result['error']}")

        return result

    def stop_server(self):
        """Gracefully stop the background uvicorn process."""
        if self._deployer:
            self._deployer.stop()
            self.log("Server stopped.")
