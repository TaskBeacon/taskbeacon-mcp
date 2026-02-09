from __future__ import annotations

from typing import Optional

from edge_tts import VoicesManager


async def _list_supported_voices_async(filter_lang: Optional[str] = None) -> list[dict]:
    vm = await VoicesManager.create()
    voices = vm.voices
    if filter_lang:
        voices = [v for v in voices if v.get("Locale", "").startswith(filter_lang)]
    return voices


async def list_supported_voices(filter_lang: Optional[str] = None, human_readable: bool = False):
    """Query available edge-tts voices.

    Parameters
    ----------
    filter_lang:
        Return only voices whose locale starts with this prefix.
    human_readable:
        If True, return a formatted table string; otherwise return the raw dict list.
    """
    voices = await _list_supported_voices_async(filter_lang)
    if not human_readable:
        return voices

    header = "{short:25} {loc:10} {gen:8} {pers:30} {name}".format(
        short="ShortName",
        loc="Locale",
        gen="Gender",
        pers="Personalities",
        name="FriendlyName",
    )
    separator = "-" * len(header)
    lines = [header, separator]

    for v in voices:
        short = (v.get("ShortName", "") or "")[:25]
        loc = (v.get("Locale", "") or "")[:10]
        gen = (v.get("Gender", "") or "")[:8]
        pers_list = (v.get("VoiceTag", {}) or {}).get("VoicePersonalities", []) or []
        pers = ", ".join(pers_list)[:30]
        disp = v.get("FriendlyName") or v.get("Name") or ""
        lines.append("{short:25} {loc:10} {gen:8} {pers:30} {disp}".format(
            short=short, loc=loc, gen=gen, pers=pers, disp=disp
        ))

    return "\n".join(lines)

