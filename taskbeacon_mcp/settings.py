from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

# GitHub org holding the template repositories.
ORG = "TaskBeacon"

# Local clone cache (relative to current working directory, as before).
CACHE = Path("./task_cache")

# Repositories that should not be treated as task templates.
NON_TASK_REPOS = {
    "task-registry",
    ".github",
    "psyflow",
    "taskbeacon-mcp",
    "community",
    "taskbeacon.github.io",
}

# Shared YAML loader/dumper instance (kept for compatibility).
yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

