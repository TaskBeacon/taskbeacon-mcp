from __future__ import annotations

from pathlib import Path


def delete_voice_mp3(assets_dir: Path) -> list[Path]:
    """Delete only files matching ``*_voice.mp3`` inside an assets directory."""
    removed: list[Path] = []
    if not assets_dir.exists():
        return removed
    for f in assets_dir.glob("*_voice.mp3"):
        f.unlink()
        removed.append(f)
    return removed


def read_config_yaml(task_path: Path) -> tuple[Path, str]:
    cfg_path = task_path / "config" / "config.yaml"
    if not cfg_path.exists():
        raise FileNotFoundError("config.yaml not found in given path.")
    return cfg_path, cfg_path.read_text(encoding="utf-8")

