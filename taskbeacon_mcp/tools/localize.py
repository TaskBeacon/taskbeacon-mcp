from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from taskbeacon_mcp.core.fs_ops import delete_voice_mp3, read_config_yaml
from taskbeacon_mcp.core.language import get_lang_code
from taskbeacon_mcp.core.prompts import localize_prompt_messages
from taskbeacon_mcp.core.voices import list_supported_voices
from taskbeacon_mcp.settings import CACHE


async def localize(task_path: str, target_language: str, voice: Optional[str] = None) -> Dict:
    """Load config.yaml and return prompt_messages for LLM localization."""
    CACHE.mkdir(exist_ok=True)

    assets_path = Path(task_path) / "assets"
    if assets_path.exists():
        delete_voice_mp3(assets_path)

    cfg_path, yaml_text = read_config_yaml(Path(task_path))

    if voice:
        voice_options = voice
    else:
        lang_code = get_lang_code(target_language)
        voice_options = await list_voices(filter_lang=lang_code)

    msgs = localize_prompt_messages(yaml_text, target_language, str(cfg_path), voice_options)
    return {"prompt_messages": [m.dict() for m in msgs], "save_path": str(cfg_path)}


async def list_voices(filter_lang: Optional[str] = None) -> str:
    lang_code = get_lang_code(filter_lang) if filter_lang else None
    return await list_supported_voices(filter_lang=lang_code, human_readable=True)

