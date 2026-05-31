from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkflowPaths:
    root: Path
    data_root: Path
    unmapped_dir: Path
    mapped_dir: Path
    sources_dir: Path
    suggestions_dir: Path
    technologies_csv: Path
    processes_csv: Path

    @classmethod
    def from_repo_root(cls, repo_root: Path) -> "WorkflowPaths":
        data_root = repo_root / "dev" / "workflow_data"
        return cls(
            root=repo_root,
            data_root=data_root,
            unmapped_dir=data_root / "unmapped_records",
            mapped_dir=data_root / "mapped_records",
            sources_dir=data_root / "sources",
            suggestions_dir=data_root / "suggestions",
            technologies_csv=data_root / "technologies.csv",
            processes_csv=data_root / "processes.csv",
        )


def detect_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (candidate / "README.md").exists() and (candidate / "dev").exists():
            return candidate
    raise FileNotFoundError("Could not detect repository root from current path.")
