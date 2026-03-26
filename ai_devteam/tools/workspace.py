"""
AI DevTeam — Phase 3: Workspace Manager
========================================
Design: Each user requirement gets its own timestamped workspace folder.
All agent outputs (documents, code files) are written into this workspace
so the entire project is persisted on disk and can be reviewed or handed off.

Workspace structure:
  workspaces/
    <project_slug>_<timestamp>/
      00_project_charter.md       ← Project Manager
      01_requirements.md          ← Business Analyst
      02_ux_spec.md               ← UI/UX Designer
      03_architecture.md          ← Architect
      04_src/                     ← Solution Developer (actual code files)
      05_test_plan.md             ← Tester
      06_deployment/              ← Deployment Engineer
      07_uat_report.md            ← UAT Validator
      pipeline.log                ← Timeline of all agent runs
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional


class Workspace:
    """Manages a single project workspace on disk."""

    # Maps agent name → output file/folder prefix
    AGENT_OUTPUTS = {
        "project_manager":      ("00_project_charter.md",  "file"),
        "business_analyst":     ("01_requirements.md",     "file"),
        "ux_designer":          ("02_ux_spec.md",          "file"),
        "architect":            ("03_architecture.md",     "file"),
        "developer":            ("04_src",                 "folder"),
        "tester":               ("05_test_plan.md",        "file"),
        "deployment_engineer":  ("06_deployment",          "folder"),
        "uat_validator":        ("07_uat_report.md",       "file"),
    }

    def __init__(self, workspace_path: Path):
        self.path = workspace_path
        self.path.mkdir(parents=True, exist_ok=True)
        # Ensure src and deployment folders exist
        (self.path / "04_src").mkdir(exist_ok=True)
        (self.path / "06_deployment").mkdir(exist_ok=True)
        self.log_path = self.path / "pipeline.log"

    @classmethod
    def create(cls, requirement: str, base_dir: Optional[str] = None) -> "Workspace":
        """Create a new workspace for a given requirement."""
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(__file__), "..", "workspaces")
        base = Path(base_dir).resolve()
        base.mkdir(parents=True, exist_ok=True)

        # Slugify the requirement into a short folder name
        slug = re.sub(r"[^a-z0-9]+", "_", requirement.lower())[:40].strip("_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{slug}_{timestamp}"
        workspace_path = base / folder_name

        ws = cls(workspace_path)
        ws.log(f"Workspace created for requirement: {requirement}")

        # Save the original requirement
        (workspace_path / "requirement.txt").write_text(requirement, encoding="utf-8")
        return ws

    @classmethod
    def load(cls, workspace_path: str) -> "Workspace":
        """Load an existing workspace by path."""
        return cls(Path(workspace_path))

    def log(self, message: str) -> None:
        """Append a timestamped entry to the pipeline log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"  📋 {message}")

    def save_agent_output(self, agent_name: str, content: str) -> Path:
        """
        Save an agent's output to the appropriate file in the workspace.
        For the developer and deployment_engineer, this saves to their folder.
        For all others, this saves to a single markdown file.
        Returns the path where the content was saved.
        """
        if agent_name not in self.AGENT_OUTPUTS:
            # Fallback: save to a generic file
            out_path = self.path / f"{agent_name}_output.md"
            out_path.write_text(content, encoding="utf-8")
            self.log(f"Saved {agent_name} output → {out_path.name}")
            return out_path

        filename, kind = self.AGENT_OUTPUTS[agent_name]

        if kind == "file":
            out_path = self.path / filename
            out_path.write_text(content, encoding="utf-8")
            self.log(f"Saved {agent_name} output → {filename}")
            return out_path
        else:
            # For folder-type agents, extract and save individual files
            folder = self.path / filename
            folder.mkdir(exist_ok=True)
            saved_files = self._extract_and_save_code_files(content, folder, agent_name)
            if not saved_files:
                # No code blocks found — save the whole response as a markdown doc
                fallback = folder / "output.md"
                fallback.write_text(content, encoding="utf-8")
                self.log(f"Saved {agent_name} output → {filename}/output.md")
                return fallback
            return folder

    def _extract_and_save_code_files(self, content: str, folder: Path, agent_name: str) -> list:
        """
        Parse the agent's response and extract code blocks with filenames.
        Looks for patterns like:
          ### filename.py
          ```python
          <code>
          ```
        or:
          **`filename.py`**
          ```python
          <code>
          ```
        Returns a list of saved file paths.
        """
        saved = []

        # Pattern 1: ### filename.ext followed by a code block
        pattern1 = re.compile(
            r'(?:#{1,4}\s+[`*]*([a-zA-Z0-9_/.\-]+\.[a-zA-Z0-9]+)[`*]*\s*\n)'
            r'(?:```[a-zA-Z]*\n)(.*?)(?:```)',
            re.DOTALL
        )

        # Pattern 2: **`filename.ext`** followed by a code block
        pattern2 = re.compile(
            r'(?:\*\*[`]([a-zA-Z0-9_/.\-]+\.[a-zA-Z0-9]+)[`]\*\*\s*\n)'
            r'(?:```[a-zA-Z]*\n)(.*?)(?:```)',
            re.DOTALL
        )

        # Pattern 3: filename.ext on its own line followed by a code block
        pattern3 = re.compile(
            r'(?:^([a-zA-Z0-9_/.\-]+\.[a-zA-Z0-9]+)\s*\n)'
            r'(?:```[a-zA-Z]*\n)(.*?)(?:```)',
            re.DOTALL | re.MULTILINE
        )

        matches = (
            list(pattern1.finditer(content)) +
            list(pattern2.finditer(content)) +
            list(pattern3.finditer(content))
        )

        seen_files = set()
        for match in matches:
            filename = match.group(1).strip()
            code = match.group(2).strip()

            # Avoid duplicate filenames
            if filename in seen_files:
                continue
            seen_files.add(filename)

            # Sanitise path — prevent directory traversal
            safe_name = Path(filename).name
            out_path = folder / safe_name
            out_path.write_text(code, encoding="utf-8")
            saved.append(out_path)
            self.log(f"  → Wrote {agent_name} file: {filename}")

        return saved

    def read_agent_output(self, agent_name: str) -> Optional[str]:
        """Read a previously saved agent output as a string."""
        if agent_name not in self.AGENT_OUTPUTS:
            return None

        filename, kind = self.AGENT_OUTPUTS[agent_name]

        if kind == "file":
            out_path = self.path / filename
            if out_path.exists():
                return out_path.read_text(encoding="utf-8")
        else:
            folder = self.path / filename
            output_md = folder / "output.md"
            if output_md.exists():
                return output_md.read_text(encoding="utf-8")
            # Concatenate all files in the folder
            if folder.exists():
                parts = []
                for f in sorted(folder.iterdir()):
                    if f.is_file():
                        parts.append(f"### {f.name}\n```\n{f.read_text(encoding='utf-8')}\n```")
                return "\n\n".join(parts) if parts else None
        return None

    def get_summary(self) -> dict:
        """Return a summary of what has been saved in this workspace."""
        summary = {
            "workspace": str(self.path),
            "requirement": (self.path / "requirement.txt").read_text(encoding="utf-8").strip()
                           if (self.path / "requirement.txt").exists() else "Unknown",
            "agents_completed": [],
            "files": [],
        }
        for agent_name, (filename, kind) in self.AGENT_OUTPUTS.items():
            target = self.path / filename
            if target.exists():
                summary["agents_completed"].append(agent_name)
                if kind == "file":
                    summary["files"].append(str(target.relative_to(self.path)))
                else:
                    for f in sorted(target.iterdir()):
                        if f.is_file():
                            summary["files"].append(str(f.relative_to(self.path)))
        return summary

    def print_summary(self) -> None:
        """Print a formatted summary of the workspace."""
        s = self.get_summary()
        print("\n" + "=" * 60)
        print("  Workspace Summary")
        print("=" * 60)
        print(f"  Path       : {s['workspace']}")
        print(f"  Requirement: {s['requirement'][:80]}")
        print(f"  Completed  : {len(s['agents_completed'])} / 8 agents")
        print("\n  Files written:")
        for f in s["files"]:
            print(f"    ✓ {f}")
        print("=" * 60 + "\n")
