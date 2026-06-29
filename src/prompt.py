from enum import Enum


class MobilityArchetype(Enum):
    NON_COMMUTER = "Non-Commuter"
    PARENT_COMMUTER = "Parent Commuter"
    FLEXIBLE_COMMUTER = "Flexible Commuter"
    RIGID_COMMUTER = "Rigid Commuter"


class ChargingArchetype(Enum):
    HABITUAL_LOW_EFFORT = "Habitual / Low-effort"
    INFORMATION_SEEKING = "Information-seeking"
    RELIABILITY_SEEKING_RISK_AVERSE = "Reliability-seeking / Risk-averse"
    ADAPTIVE_FLEXIBLE = "Adaptive / Flexible"


SYSTEM_PROMPT_INTRO: str = """You are an LLM agent simulating one EV driver's daily behavior in a transportation model.

Use the mobility archetype to shape typical stops, timing, trip chaining, and schedule flexibility. Use the charging archetype to shape charging-specific preferences when one is defined. Keep both archetype sections consistent with any persona, profile, vehicle state, map tools, and simulation rules supplied elsewhere."""


def _read_prompt(file_path: str) -> str:
    with open(file_path) as file:
        return file.read().strip()


def load_system_prompt(mobility_archetype: MobilityArchetype, charging_archetype: ChargingArchetype | str) -> str:
    mobility_prompt = _read_prompt(f"archetypes/mobility/{mobility_archetype.name.lower()}.md")
    if isinstance(charging_archetype, ChargingArchetype):
        charging_file = charging_archetype.name.lower()
    else:
        charging_file = charging_archetype
    charging_prompt = _read_prompt(f"archetypes/charging/{charging_file}.md")

    return f"""{SYSTEM_PROMPT_INTRO}

## Mobility Archetype

{mobility_prompt}

## Charging Archetype

{charging_prompt}"""
