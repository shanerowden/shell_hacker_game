from collections import defaultdict, namedtuple
from pprint import pprint as pp
from pathlib import Path
from typing import Union
import json

class DummyData:
    default_msgs = dict(
        win_condition=("You successfully completed the objective", 0),
        fail_condition=("You fucked up the mission", 0)
    )


class ClockEvent:
    """
    A Base Class for General Events on the Game Clock. Varies a bit from its children classes sometimes.
    See docstring for class.
    """
    Consequence = namedtuple("Consequence", ['attr', 'adjust'])
    EventTypes = ['warning', 'tutorial', 'objective']

    def __init__(self, hour: int,
                 msg: Union[dict, str, None],
                 event_type: str,
                 consequences: Union[list, None] = None,
                 hint: Union[str, None] = None):
        self.hour = hour
        self.msg = msg if type(msg) == str else ""
        self.event_type = event_type if event_type in ClockEvent.EventTypes else ""
        self.hint = hint if hint else "A hint is not available."
        self.consequences = [ClockEvent.Consequence(attr=attr, adjust=int(adjust))
                             for attr, adjust in consequences] if consequences else []

    def __repr__(self):
        return f'ClockEvent{self.hour}(Message: {self.msg}, Type: {self.event_type}, ' \
               + f'Consequences: {bool(self.consequences)})'


class ObjectiveEvent(ClockEvent):
    """
    Provide Hour Issued, Hours to Live, Message Dict as shown by DummyData.default_msgs
    """
    def __init__(self, hour: int,
                 msg: Union[dict, None] = None,
                 event_type: str = "objective",
                 consequences: Union[list, None] = None,
                 hours_total: Union[int, None] = None, **kwargs):
        super().__init__(hour=hour, msg=msg, event_type=event_type, consequences=consequences, **kwargs)
        self.msg = DummyData.default_msgs if msg is None else msg if type(msg) == dict else {}
        self.consequences = [] if consequences is None else consequences
        self.event_type = event_type if event_type in ClockEvent.EventTypes else "error"
        self.hour = hour
        self.hours_total = hours_total if type(hours_total) == int else 0
        self.expire_hour = self._get_expire_time(hour, hours_total)

    def __repr__(self):
        return f'ObjectimeEvent(Issued: {self.hour}, Expires: {self.expire_hour})'

    @staticmethod
    def _get_expire_time(hour_issued: int, time_till_expire: int):
        return hour_issued + time_till_expire



class PhaseClock:
    def __init__(self, total_time: int, phase_name: str, json_path: Path):
        self.total_time = total_time
        self.current_time = 0
        self.remaining_time = self._update_remaining_time()
        self.phase_name = phase_name
        self.clock = defaultdict(dict)
        self.outdated_events = defaultdict()
        self.json_data = self.get_phase_mark_json(json_path)
        self.set_json_marks_to_clock(self.json_data)
        self.next_event = self._get_most_time_sensitive_event()

    def __repr__(self):
        return f"PhaseClock({self.phase_name} - {self.remaining_time} Hours Remain in Phase)"

    def _update_remaining_time(self):
        return self.total_time - self.current_time

    def advance_clock(self, time_elapsing: int):
        marked_for_delete = []
        if self.current_time <= self.total_time:
            for hour, event in self.clock.items():
                if hour < self.current_time + 1:
                    assert self.current_time+time_elapsing != hour
                    self.outdated_events.setdefault(hour, event)
                    self.outdated_events[hour].notice = "failure"
                    marked_for_delete.append(hour)

        self.current_time += time_elapsing

        for hour in marked_for_delete:
            del self.clock[hour]

        self.next_event = self._get_most_time_sensitive_event()
        self.remaining_time = self._update_remaining_time()

    def _get_most_time_sensitive_event(self):
        for hour, event in self.clock.items():
            if not self.clock[hour].consequences:
                continue
            if self.clock[hour].consequences:
                return event

    @staticmethod
    def get_phase_mark_json(p):
        try:
            with open(p) as fo:
                return json.load(fo)
        except FileNotFoundError as exc:
            raise exc

    # Helper Functions
    def set_json_marks_to_clock(self, json_data: dict):
        for idx, mark in enumerate(json_data["events"]):
            conseqs_to_obj = [ClockEvent.Consequence(
                attr=mark["consequences"][c_idx]['attr'],
                adjust=mark["consequences"][c_idx]['adjust']
             ) for c_idx, _ in enumerate(mark["consequences"])]

            assert type(conseqs_to_obj) == list
            event = ClockEvent(mark['hour'], mark['msg'], mark['event_type'], conseqs_to_obj, mark['hint'])
            self.clock.setdefault(event.hour, event)


# Needs to Go into aNother Module
p1 = PhaseClock(168, "One Week Till Termination", Path(
    "shellmancer", "game", "one_week_till_term_phase1.json"
).resolve())

# Just Testing
p1.advance_clock(1)
pp(p1.next_event)
pp(p1.clock)

o = ObjectiveEvent(hour=1, msg=DummyData.default_msgs, hours_total=3)
