import sys

sys.path.insert(0, "src")

from rule_simulation import RuleAgent, SCHEDULE, Schedule
from utils import parse_environment


def test_default_schedule_terminates() -> None:
    agent = RuleAgent(
        schedule = Schedule(blocks = SCHEDULE, start_time = 0),
        soc_kwh = 50,
        battery_capacity = 80
    )

    events = agent.run(parse_environment())

    assert events[-1]["status"] == "at_location"
    assert events[-1]["location"] == "office"


def test_travel_event_uses_updated_soc() -> None:
    schedule = Schedule(
        blocks = [
            {"location": "home", "dwell_time": 0},
            {"location": "office", "dwell_time": 0}
        ],
        start_time = 0
    )
    agent = RuleAgent(schedule = schedule, soc_kwh = 50, battery_capacity = 80)

    events = agent.run(parse_environment(), step = 5)

    first_travel = next(event for event in events if event["status"] == "traveling")
    assert first_travel["soc_kwh"] < 50


def test_public_charger_increases_soc() -> None:
    schedule = Schedule(
        blocks = [
            {"location": "public_charger", "dwell_time": 10}
        ],
        start_time = 0
    )
    agent = RuleAgent(schedule = schedule, soc_kwh = 50, battery_capacity = 80)

    agent.run(parse_environment(), step = 5)

    assert agent.soc_kwh > 50


def test_public_charger_caps_at_battery_capacity() -> None:
    schedule = Schedule(
        blocks = [
            {"location": "public_charger", "dwell_time": 10}
        ],
        start_time = 0
    )
    agent = RuleAgent(schedule = schedule, soc_kwh = 75, battery_capacity = 80)

    agent.run(parse_environment(), step = 5)

    assert agent.soc_kwh == 80
