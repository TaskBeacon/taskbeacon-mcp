from __future__ import annotations

from pathlib import Path

from git import Repo

from taskbeacon_mcp.settings import CACHE, ORG


def clone(repo: str, org: str = ORG, cache_dir: Path = CACHE) -> Path:
    dest = cache_dir / repo
    if dest.exists():
        return dest
    Repo.clone_from("https://github.com/{org}/{repo}.git".format(org=org, repo=repo), dest, depth=1)
    return dest

