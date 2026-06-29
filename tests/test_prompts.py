import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt import (
    CHARGING_PROMPT_DIR,
    MOBILITY_PROMPT_PATHS,
    SYSTEM_PROMPT_INTRO,
    MobilityArchetype,
    load_system_prompt
)

FORBIDDEN_MOBILITY_PATTERNS: list[str] = [
    r"\bcharge\b",
    r"\bcharges\b",
    r"\bcharged\b",
    r"\bcharging\b",
    r"\bcharger\b",
    r"\bchargers\b",
    r"\bbattery\b",
    r"\bbatteries\b",
    r"\bkwh\b",
    r"\bl1\b",
    r"\bl2\b",
    r"\bdc\b"
]


def test_load_system_prompt_for_every_mobility_archetype() -> None:
    for archetype in MobilityArchetype:
        prompt_text = load_system_prompt(archetype)
        mobility_prompt = MOBILITY_PROMPT_PATHS[archetype].read_text().strip()
        charging_prompt = (CHARGING_PROMPT_DIR / "placeholder.md").read_text().strip()

        assert prompt_text.startswith(SYSTEM_PROMPT_INTRO)
        assert "## Mobility Archetype" in prompt_text
        assert "## Charging Archetype" in prompt_text
        assert mobility_prompt in prompt_text
        assert charging_prompt in prompt_text
        assert archetype.value in prompt_text


def test_unknown_charging_archetype_raises_file_not_found() -> None:
    try:
        load_system_prompt(MobilityArchetype.NON_COMMUTER, charging_archetype = "missing")
        raise AssertionError("expected FileNotFoundError")
    except FileNotFoundError as error:
        assert "missing.md" in str(error)


def test_mobility_prompts_do_not_include_charging_behavior() -> None:
    for path in MOBILITY_PROMPT_PATHS.values():
        text = path.read_text().lower()
        for forbidden_pattern in FORBIDDEN_MOBILITY_PATTERNS:
            assert re.search(forbidden_pattern, text) is None
