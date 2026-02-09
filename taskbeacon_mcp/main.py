"""
Compatibility entrypoint.

Historically, the console script pointed at ``taskbeacon_mcp.main:main``.
The server wiring now lives in ``taskbeacon_mcp.server``; this module keeps
that import path stable.
"""

from __future__ import annotations

from pathlib import Path
import sys


def _ensure_repo_root_on_syspath() -> None:
    """
    Allow running this file directly (e.g. ``python taskbeacon_mcp/main.py``).

    When executed as a script, Python puts the package directory itself on
    ``sys.path``; importing ``taskbeacon_mcp`` then fails because the parent
    (repo root) is missing.
    """

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


try:
    from taskbeacon_mcp.server import main, mcp
except ModuleNotFoundError as e:  # pragma: no cover
    # Only treat missing top-level package as a path issue; dependency errors
    # should still surface to the caller.
    if e.name != "taskbeacon_mcp":
        raise
    _ensure_repo_root_on_syspath()
    from taskbeacon_mcp.server import main, mcp

__all__ = ["main", "mcp"]


if __name__ == "__main__":
    main()
