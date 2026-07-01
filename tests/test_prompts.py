import re
import sys

sys.path.insert(0, "src")

from prompt import (
    SYSTEM_PROMPT_INTRO,
    ChargingArchetype,
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

FORBIDDEN_MOBILITY_DAY_PATTERNS: list[str] = [
    r"\bweekday\b",
    r"\bweekdays\b",
    r"\bweekend\b",
    r"\bweekends\b"
]

CHARGING_SCORE_LABELS: list[str] = [
    "Information Engagement",
    "Risk Buffer Preference",
    "Adaptive Flexibility",
    "Cost/Effort Willingness"
]


def read_prompt(file_path: str) -> str:
    with open(file_path) as file:
        return file.read().strip()


def mobility_prompt_file(mobility_archetype: MobilityArchetype) -> str:
    return f"archetypes/mobility/{mobility_archetype.name.lower()}.md"


def charging_prompt_file(charging_archetype: ChargingArchetype) -> str:
    return f"archetypes/charging/{charging_archetype.name.lower()}.md"


def test_load_system_prompt_for_every_archetype_pair() -> None:
    for mobility_archetype in MobilityArchetype:
        for charging_archetype in ChargingArchetype:
            prompt_text = load_system_prompt(mobility_archetype, charging_archetype)
            mobility_prompt = read_prompt(mobility_prompt_file(mobility_archetype))
            charging_prompt = read_prompt(charging_prompt_file(charging_archetype))

            assert prompt_text.startswith(SYSTEM_PROMPT_INTRO)
            assert "## Mobility Archetype" in prompt_text
            assert "## Charging Archetype" in prompt_text
            assert mobility_prompt in prompt_text
            assert charging_prompt in prompt_text
            assert mobility_archetype.value in prompt_text
            assert charging_archetype.value in prompt_text


def test_load_system_prompt_requires_charging_archetype() -> None:
    try:
        load_system_prompt(MobilityArchetype.NON_COMMUTER)
        raise AssertionError("expected TypeError")
    except TypeError as error:
        assert "charging_archetype" in str(error)


def test_unknown_charging_archetype_raises_file_not_found() -> None:
    try:
        load_system_prompt(MobilityArchetype.NON_COMMUTER, charging_archetype = "missing")
        raise AssertionError("expected FileNotFoundError")
    except FileNotFoundError as error:
        assert "missing.md" in str(error)


def test_mobility_prompts_do_not_include_charging_behavior() -> None:
    for mobility_archetype in MobilityArchetype:
        text = read_prompt(mobility_prompt_file(mobility_archetype)).lower()
        for forbidden_pattern in FORBIDDEN_MOBILITY_PATTERNS:
            assert re.search(forbidden_pattern, text) is None


def test_mobility_prompts_do_not_include_day_type_terms() -> None:
    for mobility_archetype in MobilityArchetype:
        text = read_prompt(mobility_prompt_file(mobility_archetype)).lower()
        for forbidden_pattern in FORBIDDEN_MOBILITY_DAY_PATTERNS:
            assert re.search(forbidden_pattern, text) is None


def test_charging_prompts_include_score_dimensions() -> None:
    for charging_archetype in ChargingArchetype:
        text = read_prompt(charging_prompt_file(charging_archetype))
        assert charging_archetype.value in text
        for score_label in CHARGING_SCORE_LABELS:
            assert score_label in text
