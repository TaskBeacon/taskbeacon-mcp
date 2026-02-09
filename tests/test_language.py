from taskbeacon_mcp.core.language import get_lang_code


def test_get_lang_code_direct_key_and_value() -> None:
    assert get_lang_code("english") == "en"
    assert get_lang_code("us english") == "en-US"
    assert get_lang_code("EN-us") == "en-US"


def test_get_lang_code_fuzzy_and_none() -> None:
    assert get_lang_code("englsh") == "en"
    assert get_lang_code("not-a-language") is None

