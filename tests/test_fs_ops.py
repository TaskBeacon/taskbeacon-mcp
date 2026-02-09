from pathlib import Path

from taskbeacon_mcp.core.fs_ops import delete_voice_mp3


def test_delete_voice_mp3_only_matches_pattern(tmp_path: Path) -> None:
    assets = tmp_path / "assets"
    assets.mkdir()

    (assets / "a_voice.mp3").write_text("x", encoding="utf-8")
    (assets / "b_voice.mp3").write_text("x", encoding="utf-8")
    (assets / "notvoice.mp3").write_text("x", encoding="utf-8")
    (assets / "c_voice.wav").write_text("x", encoding="utf-8")

    removed = delete_voice_mp3(assets)
    removed_names = {p.name for p in removed}
    assert removed_names == {"a_voice.mp3", "b_voice.mp3"}

    assert (assets / "notvoice.mp3").exists()
    assert (assets / "c_voice.wav").exists()
