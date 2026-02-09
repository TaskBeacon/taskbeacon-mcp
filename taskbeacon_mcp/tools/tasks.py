from __future__ import annotations

import asyncio
from typing import Dict, List, Optional

from taskbeacon_mcp.core.github_api import fetch_readme_snippet, repo_branches, task_repos
from taskbeacon_mcp.core.git_ops import clone
from taskbeacon_mcp.core.prompts import (
    choose_repo_prompt_messages,
    choose_template_prompt_messages,
    render_prompt,
)
from taskbeacon_mcp.settings import CACHE, NON_TASK_REPOS, ORG


async def build_task(target_task: str, source_task: Optional[str] = None) -> Dict:
    """With `source_task` -> clone repo & return prompt + local path.

    Without `source_task` -> return prompt_messages so the LLM can choose a template.
    """
    CACHE.mkdir(exist_ok=True)
    repos = await task_repos(ORG, NON_TASK_REPOS)

    if source_task:
        repo = next((r for r in repos if source_task.lower() in r.lower()), None)
        if not repo:
            raise ValueError("Template repo not found.")
        path = await asyncio.to_thread(clone, repo)
        prompt = render_prompt("transform.md", source_task=source_task, target_task=target_task)
        return {"prompt": prompt, "template_path": str(path)}

    snippets: list[dict] = []
    for repo in repos:
        snippet = await fetch_readme_snippet(ORG, repo, branch="main", limit_chars=2000)
        snippets.append({"repo": repo, "readme_snippet": snippet})

    msgs = choose_template_prompt_messages("A {t} task.".format(t=target_task), snippets)
    return {
        "prompt_messages": [m.dict() for m in msgs],
        "note": "Reply with chosen repo, then call build_task again with source_task=<repo>.",
    }


async def download_task(repo: str) -> Dict:
    """Clone any template repo locally and return the path.

    If `repo` is ambiguous (or natural language), return prompt_messages so the LLM can choose.
    """
    CACHE.mkdir(exist_ok=True)
    all_repos = await task_repos(ORG, NON_TASK_REPOS)

    if repo in all_repos:
        path = await asyncio.to_thread(clone, repo)
        return {"template_path": str(path)}

    snippets: list[dict] = []
    for r_name in all_repos:
        snippet = await fetch_readme_snippet(ORG, r_name, branch="main", limit_chars=2000)
        snippets.append({"repo": r_name, "readme_snippet": snippet})

    msgs = choose_repo_prompt_messages(repo, snippets)
    return {
        "prompt_messages": [m.dict() for m in msgs],
        "note": "Reply with chosen repo, then call download_task again with the selected repo name.",
    }


async def list_tasks() -> List[Dict]:
    """Return metadata for every task template repo."""
    repos = await task_repos(ORG, NON_TASK_REPOS)

    async def build_entry(repo: str) -> Dict:
        snippet = await fetch_readme_snippet(ORG, repo, branch="main", limit_chars=2000)
        branches = await repo_branches(ORG, repo, limit=20)
        return {"repo": repo, "readme_snippet": snippet, "branches": branches}

    return await asyncio.gather(*(build_entry(r) for r in repos))

