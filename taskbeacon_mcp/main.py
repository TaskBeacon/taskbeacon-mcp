"""
Compatibility entrypoint.

Historically, the console script pointed at ``taskbeacon_mcp.main:main``.
The server wiring now lives in ``taskbeacon_mcp.server``; this module keeps
that import path stable.
"""

from __future__ import annotations

from taskbeacon_mcp.server import main, mcp

__all__ = ["main", "mcp"]


if __name__ == "__main__":
    main()

