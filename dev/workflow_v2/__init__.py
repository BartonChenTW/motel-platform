"""MOTEL Workflow v2 implementation package.

This package provides an end-to-end vertical slice for:
- record submission
- mapping suggestion
- deduplication
- reviewer approval
"""

from .pipeline import WorkflowEngine
from .settings import WorkflowPaths

__all__ = ["WorkflowEngine", "WorkflowPaths"]
