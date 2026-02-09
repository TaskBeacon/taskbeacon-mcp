from __future__ import annotations

from importlib import resources
from typing import Optional

from mcp.server.fastmcp.prompts.base import Message, UserMessage


def load_prompt(name: str) -> str:
    fname = name if name.endswith(".md") else "{name}.md".format(name=name)
    text = (
        resources.files("taskbeacon_mcp")
        .joinpath("prompts")
        .joinpath(fname)
        .read_text(encoding="utf-8")
    )
    return text.strip()


def render_prompt(name: str, **fields: object) -> str:
    return load_prompt(name).format(**fields)


def choose_template_prompt_messages(desc: str, candidates: list[dict]) -> list[Message]:
    intro = render_prompt("choose_template_intro.md")
    menu = "\n".join(["- **{repo}**: {snippet}".format(
        repo=c.get("repo", ""),
        snippet=c.get("readme_snippet", ""),
    ) for c in candidates]) or "(no templates found)"
    return [
        UserMessage(intro),
        UserMessage("Desired task:\n{desc}".format(desc=desc)),
        UserMessage("Candidate templates:\n{menu}".format(menu=menu)),
    ]


def choose_repo_prompt_messages(user_query: str, candidates: list[dict]) -> list[Message]:
    intro = render_prompt("choose_repo_intro.md")
    menu = "\n".join(["- **{repo}**: {snippet}".format(
        repo=c.get("repo", ""),
        snippet=c.get("readme_snippet", ""),
    ) for c in candidates]) or "(no repositories found)"
    return [
        UserMessage(intro),
        UserMessage("User query: {q}".format(q=user_query)),
        UserMessage("Candidate repositories:\n{menu}".format(menu=menu)),
    ]


def localize_prompt_messages(
    yaml_text: str,
    target_language: str,
    cfg_path: str,
    voice_options: Optional[str] = None,
) -> list[Message]:
    voice_block = ""
    if voice_options:
        voice_block = render_prompt(
            "localize_voice.md",
            target_language=target_language,
            voice_options=voice_options,
        )
    intro = render_prompt(
        "localize_intro.md",
        target_language=target_language,
        cfg_path=cfg_path,
        voice_block=voice_block,
    )
    return [UserMessage(intro), UserMessage(yaml_text)]

