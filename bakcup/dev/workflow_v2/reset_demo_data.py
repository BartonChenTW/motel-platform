from __future__ import annotations

from pathlib import Path

from .bootstrap import bootstrap_demo_records
from .settings import WorkflowPaths, detect_repo_root


def reset_demo_data() -> None:
    repo_root = detect_repo_root(Path(__file__).resolve())
    paths = WorkflowPaths.from_repo_root(repo_root)

    for folder in [paths.unmapped_dir, paths.mapped_dir, paths.suggestions_dir]:
        folder.mkdir(parents=True, exist_ok=True)
        for item in folder.glob("*"):
            if item.is_file():
                item.unlink(missing_ok=True)

    bootstrap_demo_records()


if __name__ == "__main__":
    reset_demo_data()
