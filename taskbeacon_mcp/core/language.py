from __future__ import annotations

from typing import Optional

from fuzzywuzzy import process

LANGUAGE_MAP = {
    "arabic": "ar",
    "egyptian arabic": "ar-EG",
    "saudi arabic": "ar-SA",
    "bengali": "bn",
    "bulgarian": "bg",
    "catalan": "ca",
    "mandarin chinese": "zh-CN",
    "taiwanese chinese": "zh-TW",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "australian english": "en-AU",
    "canadian english": "en-CA",
    "uk english": "en-GB",
    "us english": "en-US",
    "estonian": "et",
    "filipino": "fil",
    "finnish": "fi",
    "french": "fr",
    "canadian french": "fr-CA",
    "german": "de",
    "austrian german": "de-AT",
    "swiss german": "de-CH",
    "greek": "el",
    "gujarati": "gu",
    "hebrew": "he",
    "hindi": "hi",
    "hungarian": "hu",
    "icelandic": "is",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "kannada": "kn",
    "kazakh": "kk",
    "korean": "ko",
    "latvian": "lv",
    "lithuanian": "lt",
    "macedonian": "mk",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "marathi": "mr",
    "norwegian": "nb",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "brazilian portuguese": "pt-BR",
    "romanian": "ro",
    "russian": "ru",
    "serbian": "sr",
    "slovak": "sk",
    "slovenian": "sl",
    "spanish": "es",
    "mexican spanish": "es-MX",
    "us spanish": "es-US",
    "swahili": "sw",
    "swedish": "sv",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "vietnamese": "vi",
    "welsh": "cy",
}


def get_lang_code(lang_name: str) -> Optional[str]:
    """Find the best language code match for a natural language name.

    Matches:
    - exact language codes (case-insensitive), e.g. "en-US"
    - exact keys, e.g. "english"
    - fuzzy keys via fuzzywuzzy (threshold > 80)
    """
    if not lang_name:
        return None

    q = lang_name.strip()
    if not q:
        return None

    q_lower = q.lower()

    # Direct match in values (case-insensitive) -> return canonical value.
    for v in LANGUAGE_MAP.values():
        if v.lower() == q_lower:
            return v

    # Direct match in keys.
    if q_lower in LANGUAGE_MAP:
        return LANGUAGE_MAP[q_lower]

    # Fuzzy match among keys.
    match = process.extractOne(q_lower, LANGUAGE_MAP.keys())
    if match and match[1] > 80:
        return LANGUAGE_MAP[match[0]]

    return None


# Backwards-compatible alias (previous internal helper name).
_get_lang_code = get_lang_code

