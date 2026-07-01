import json
from typing import TypedDict, Literal

class ScheduleBlock(TypedDict):
    location: str
    dwell_time: int

class EnvEdge(TypedDict):
    from_: str
    to: str
    distance: int
    travel_time: int

Environment = list[EnvEdge]

class Event(TypedDict):
    timestamp: int
    status: Literal["at_location", "traveling"]
    location: str | None
    soc_kwh: float

def parse_environment() -> list[EnvEdge]:
    with open("src/environment.json") as file:
        environment = json.load(file)

    return [
        {
            "from_": from_location,
            "to": edge["to"],
            "distance": edge["distance"],
            "travel_time": edge["travel_time"],
        }
        for from_location, edges in environment.items()
        for edge in edges
    ]
