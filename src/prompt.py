from pathlib import Path
from enum import Enum


class MobilityArchetype(Enum):
    NON_COMMUTER = "Non-Commuter"
    PARENT_COMMUTER = "Parent Commuter"
    FLEXIBLE_COMMUTER = "Flexible Commuter"
    RIGID_COMMUTER = "Rigid Commuter"


PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
ARCHETYPE_ROOT: Path = PROJECT_ROOT / "archetypes"
MOBILITY_PROMPT_DIR: Path = ARCHETYPE_ROOT / "mobility"
CHARGING_PROMPT_DIR: Path = ARCHETYPE_ROOT / "charging"

MOBILITY_PROMPT_PATHS: dict[MobilityArchetype, Path] = {
    MobilityArchetype.NON_COMMUTER: MOBILITY_PROMPT_DIR / "non_commuter.md",
    MobilityArchetype.PARENT_COMMUTER: MOBILITY_PROMPT_DIR / "parent_commuter.md",
    MobilityArchetype.FLEXIBLE_COMMUTER: MOBILITY_PROMPT_DIR / "flexible_commuter.md",
    MobilityArchetype.RIGID_COMMUTER: MOBILITY_PROMPT_DIR / "rigid_commuter.md"
}

SYSTEM_PROMPT_INTRO: str = """You are an LLM agent simulating one EV driver's daily behavior in a transportation model.

Use the mobility archetype to shape typical stops, timing, trip chaining, and schedule flexibility. Use the charging archetype to shape charging-specific preferences when one is defined. Keep both archetype sections consistent with any persona, profile, vehicle state, map tools, and simulation rules supplied elsewhere."""


def _read_prompt(path: Path) -> str:
    return path.read_text().strip()


def load_system_prompt(mobility_archetype: MobilityArchetype, charging_archetype: str = "placeholder") -> str:
    mobility_prompt = _read_prompt(MOBILITY_PROMPT_PATHS[mobility_archetype])
    charging_prompt = _read_prompt(CHARGING_PROMPT_DIR / f"{charging_archetype}.md")

    return f"""{SYSTEM_PROMPT_INTRO}

## Mobility Archetype

{mobility_prompt}

## Charging Archetype

{charging_prompt}"""
