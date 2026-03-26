"""
AI DevTeam — Local Deployer
============================
Installs Python dependencies and starts a uvicorn server as a background
process so the pipeline ends with a live running API.

Usage (called by DeploymentEngineerAgent after code extraction):

    from tools.local_deployer import LocalDeployer

    deployer = LocalDeployer(project_dir=Path("/path/to/workspace/06_deployment/app"))
    result = deployer.deploy(port=8000)
    if result["success"]:
        print(f"Server running at {result['url']}")
    else:
        print(f"Deploy failed: {result['error']}")
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


class LocalDeployer:
    """
    Handles local deployment of a FastAPI application extracted from the pipeline.

    Steps:
      1. Locate requirements.txt and install deps via pip.
      2. Detect the FastAPI app entry point (main.py / app.py).
      3. Start uvicorn as a background subprocess.
      4. Poll the /health or / endpoint to confirm the server is up.
      5. Return the live URL and PID.
    """

    STARTUP_TIMEOUT = 30      # seconds to wait for server to respond
    POLL_INTERVAL  = 0.5      # seconds between health-check polls
    DEFAULT_PORT   = 8000

    def __init__(self, project_dir: Path, port: int = DEFAULT_PORT):
        self.project_dir = Path(project_dir).resolve()
        self.port = port
        self._process: Optional[subprocess.Popen] = None

    # ── Public API ─────────────────────────────────────────────────────────────

    def deploy(self) -> dict:
        """
        Install dependencies and start the server.
        Returns a dict with keys: success, url, pid, error.
        """
        # 1. Install dependencies
        install_result = self._install_deps()
        if not install_result["success"]:
            return {"success": False, "url": None, "pid": None,
                    "error": install_result["error"]}

        # 2. Find the app entry point
        app_module = self._detect_app_module()
        if not app_module:
            return {"success": False, "url": None, "pid": None,
                    "error": "Could not locate a FastAPI app entry point (main.py or app.py)."}

        # 3. Start uvicorn
        start_result = self._start_uvicorn(app_module)
        if not start_result["success"]:
            return {"success": False, "url": None, "pid": None,
                    "error": start_result["error"]}

        # 4. Wait for the server to respond
        url = f"http://localhost:{self.port}"
        alive = self._wait_for_server(url)
        if not alive:
            self.stop()
            return {"success": False, "url": None, "pid": None,
                    "error": f"Server did not respond within {self.STARTUP_TIMEOUT}s."}

        return {
            "success": True,
            "url": url,
            "pid": self._process.pid,
            "error": None,
        }

    def stop(self):
        """Terminate the background uvicorn process if running."""
        if self._process and self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()

    # ── Private helpers ────────────────────────────────────────────────────────

    def _install_deps(self) -> dict:
        """Install requirements.txt if present."""
        req_file = self._find_requirements()
        if not req_file:
            # No requirements file — assume deps are already installed
            return {"success": True}

        pip = self._pip_executable()
        cmd = [pip, "install", "-q", "-r", str(req_file)]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                return {"success": False,
                        "error": f"pip install failed:\n{result.stderr[:500]}"}
            return {"success": True}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "pip install timed out after 120s."}
        except FileNotFoundError:
            return {"success": False, "error": f"pip not found at: {pip}"}

    def _start_uvicorn(self, app_module: str) -> dict:
        """Launch uvicorn in the background."""
        python = sys.executable
        cmd = [
            python, "-m", "uvicorn",
            app_module,
            "--host", "0.0.0.0",
            "--port", str(self.port),
            "--reload",
        ]
        log_path = self.project_dir / "uvicorn.log"
        try:
            log_file = open(log_path, "w")
            self._process = subprocess.Popen(
                cmd,
                cwd=str(self.project_dir),
                stdout=log_file,
                stderr=log_file,
                env={**os.environ, "PYTHONPATH": str(self.project_dir)},
            )
            return {"success": True}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def _wait_for_server(self, url: str) -> bool:
        """Poll the server until it responds or timeout is reached."""
        import urllib.request
        import urllib.error

        deadline = time.time() + self.STARTUP_TIMEOUT
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(url, timeout=2) as resp:
                    if resp.status < 500:
                        return True
            except Exception:
                pass
            # Also check if the process died
            if self._process and self._process.poll() is not None:
                return False
            time.sleep(self.POLL_INTERVAL)
        return False

    def _find_requirements(self) -> Optional[Path]:
        """Search for requirements.txt in the project directory tree."""
        for candidate in [
            self.project_dir / "requirements.txt",
            self.project_dir / "backend" / "requirements.txt",
            *self.project_dir.rglob("requirements.txt"),
        ]:
            if candidate.exists():
                return candidate
        return None

    def _detect_app_module(self) -> Optional[str]:
        """
        Detect the uvicorn app module string (e.g. 'app.main:app').
        Searches for main.py or app.py containing a FastAPI() instantiation.
        """
        candidates = list(self.project_dir.rglob("main.py")) + \
                     list(self.project_dir.rglob("app.py"))

        for path in candidates:
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            if "FastAPI" not in text:
                continue

            # Build the dotted module path relative to project_dir
            rel = path.relative_to(self.project_dir)
            parts = list(rel.with_suffix("").parts)   # e.g. ['app', 'main']
            module_path = ".".join(parts)              # e.g. 'app.main'

            # Detect the app variable name (app = FastAPI() or api = FastAPI())
            app_var = "app"
            for line in text.splitlines():
                if "FastAPI()" in line or "FastAPI(" in line:
                    var = line.split("=")[0].strip()
                    if var.isidentifier():
                        app_var = var
                    break

            return f"{module_path}:{app_var}"

        return None

    @staticmethod
    def _pip_executable() -> str:
        """Return the pip executable matching the current Python interpreter."""
        pip = Path(sys.executable).parent / "pip"
        if pip.exists():
            return str(pip)
        pip3 = Path(sys.executable).parent / "pip3"
        if pip3.exists():
            return str(pip3)
        return "pip"
