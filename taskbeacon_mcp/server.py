from typing import Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message, UserMessage

from taskbeacon_mcp.core.prompts import (
    choose_repo_prompt_messages,
    choose_template_prompt_messages,
    localize_prompt_messages,
    render_prompt,
)
from taskbeacon_mcp.tools.localize import list_voices as _list_voices_tool
from taskbeacon_mcp.tools.localize import localize as _localize_tool
from taskbeacon_mcp.tools.tasks import build_task as _build_task_tool
from taskbeacon_mcp.tools.tasks import download_task as _download_task_tool
from taskbeacon_mcp.tools.tasks import list_tasks as _list_tasks_tool


# MCP server wiring only (tools/prompts are thin wrappers around core modules).
mcp = FastMCP(name="taskbeacon-mcp")


# ---------------------------------------------------------------------------
# Prompts (public MCP surface)
# ---------------------------------------------------------------------------
@mcp.prompt(title="Task Transformation Prompt")
def transform_prompt(source_task: str, target_task: str) -> UserMessage:
    content = render_prompt(
        "transform.md",
        source_task=source_task,
        target_task=target_task,
    )
    return UserMessage(content)


@mcp.prompt(title="Localize task")
def localize_prompt(
    yaml_text: str,
    target_language: str,
    cfg_path: str,
    voice_options: Optional[str] = None,
) -> list[Message]:
    return localize_prompt_messages(yaml_text, target_language, cfg_path, voice_options)


@mcp.prompt(title="Choose Template")
def choose_template_prompt(desc: str, candidates: list[dict]) -> list[Message]:
    return choose_template_prompt_messages(desc, candidates)


@mcp.prompt(title="Choose Repository for Download")
def choose_repo_prompt(user_query: str, candidates: list[dict]) -> list[Message]:
    return choose_repo_prompt_messages(user_query, candidates)


# ---------------------------------------------------------------------------
# Tools (public MCP surface)
# ---------------------------------------------------------------------------
@mcp.tool()
async def build_task(target_task: str, source_task: Optional[str] = None) -> Dict:
    return await _build_task_tool(target_task=target_task, source_task=source_task)


@mcp.tool()
async def download_task(repo: str) -> Dict:
    return await _download_task_tool(repo=repo)


@mcp.tool()
async def localize(
    task_path: str,
    target_language: str,
    voice: Optional[str] = None,
) -> Dict:
    return await _localize_tool(task_path=task_path, target_language=target_language, voice=voice)


@mcp.tool()
async def list_voices(filter_lang: Optional[str] = None) -> str:
    return await _list_voices_tool(filter_lang=filter_lang)


@mcp.tool()
async def list_tasks() -> List[Dict]:
    return await _list_tasks_tool()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
