from taskbeacon_mcp.core.prompts import render_prompt


def test_transform_prompt_contains_key_phrases() -> None:
    text = render_prompt("transform.md", source_task="SST", target_task="Stroop")
    assert "Stage 0: Plan" in text
    assert "deg" in text

