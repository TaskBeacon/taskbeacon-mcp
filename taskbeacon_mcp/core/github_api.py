from __future__ import annotations

from typing import Iterable, List, Sequence

import httpx


async def github_repos(org: str) -> List[dict]:
    url = "https://api.github.com/orgs/{org}/repos?per_page=100".format(org=org)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=30)
        resp.raise_for_status()
    return resp.json()


async def repo_branches(org: str, repo: str, limit: int = 20) -> List[str]:
    url = "https://api.github.com/repos/{org}/{repo}/branches?per_page=100".format(org=org, repo=repo)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=15)
    return [b["name"] for b in resp.json()][:limit]


async def task_repos(org: str, non_task_repos: Sequence[str] | set[str]) -> List[str]:
    repos = await github_repos(org)
    non = set(non_task_repos)
    return [r["name"] for r in repos if r.get("name") not in non]


async def fetch_readme_snippet(
    org: str,
    repo: str,
    branch: str = "main",
    limit_chars: int = 2000,
) -> str:
    url = "https://raw.githubusercontent.com/{org}/{repo}/{branch}/README.md".format(
        org=org, repo=repo, branch=branch
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
    if resp.status_code != 200:
        return ""
    return resp.text[:limit_chars].replace("\n", " ")

