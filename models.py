from typing import NamedTuple, Optional, Set
from datetime import date

class Event(NamedTuple):
    """
    A calendar entry for a conference

    TODO: add event title
    """
    start_date: date
    end_date: date
    website: Optional[str]
    description: str
    title: str


class Plan(NamedTuple):
    """
    A planned set of changes to make against the calendar API
    """
    calendar_id: int
    to_remove: Set[int]
    to_add: Set[Event]