from utils import *
from pydantic import BaseModel

SCHEDULE: list[ScheduleBlock] = [
    {"location": "home", "dwell_time": 0},
    {"location": "office", "dwell_time": 480},
    {"location": "shopping_mall", "dwell_time": 45},
    {"location": "public_charger", "dwell_time": 45},
    {"location": "office", "dwell_time": 60},
]

SOC_PER_MILE = 0.30
SOC_CHARGE_PER_MIN = 1.4

class Schedule(BaseModel):
    blocks: list[ScheduleBlock]
    start_time: int

def time_between(from_: str, to: str, env: Environment) -> int:
    return next(edge for edge in env if edge["from_"] == from_ and edge["to"] == to)["travel_time"]

def dist_between(from_: str, to: str, env: Environment) -> int:
    return next(edge for edge in env if edge["from_"] == from_ and edge["to"] == to)["distance"]

class RuleAgent(BaseModel):
    schedule: Schedule
    soc_kwh: float
    battery_capacity: float

    def run(self, env: Environment, step: int = 5) -> list[Event]:
        t = self.schedule.start_time
        events = []

        stack = self.schedule.blocks[::-1]
        dwell = 0
        arrival_time = 0
        soc_per_min = 0

        status: Literal["at_location", "traveling"] = "at_location"
        stop = stack.pop()

        while True:
            if t % step == 0:
                events.append(Event(
                    timestamp = t,
                    status = status,
                    location = stop["location"] if status == "at_location" else None,
                    soc_kwh = self.soc_kwh
                ))

            if status == "at_location":
                if dwell == stop["dwell_time"]:
                    if stack:
                        status = "traveling"
                        travel_time = time_between(stop["location"], stack[-1]["location"], env)
                        arrival_time = t + travel_time
                        soc_per_min = (SOC_PER_MILE * dist_between(stop["location"], stack[-1]["location"], env)) / travel_time
                    else:
                        return events
                else:
                    if stop["location"] == "public_charger":
                        self.soc_kwh = min(self.battery_capacity, self.soc_kwh + SOC_CHARGE_PER_MIN)

                    dwell += 1
            elif status == "traveling":
                self.soc_kwh -= soc_per_min

                if t == arrival_time:
                    status = "at_location"
                    stop = stack.pop()
                    dwell = 0

            t += 1
