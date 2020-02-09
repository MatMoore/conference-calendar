"""
Load events from CSV
Load events from Calendar
Calculate Removals, Additions
Execute
"""
from typing import NamedTuple, List, Set, Dict
from datetime import date
from csv import DictReader


HEADER_NAMES = ['start_date', 'end_date', 'website', 'description']


class Event(NamedTuple):
    """
    A calendar entry for a conference
    """
    start_date: date
    end_date: date
    website: str
    description: str


class Plan(NamedTuple):
    """
    A planned set of changes to make against the calendar API
    """
    calendar_id: int
    to_remove: Set[int]
    to_add: Set[Event]


class MalformedCSV(Exception):
    """
    Raised if the input CSV is malformed.
    """


def parse_events(csv_file) -> Set[Event]:
    """
    Parse a CSV file and return a list of events
    """
    results = set()
    csv_reader = DictReader(csv_file)

    if csv_reader.fieldnames != HEADER_NAMES:
        raise MalformedCSV(f'Expected header to equal {HEADER_NAMES} but got {csv_reader.fieldnames}')

    for row in csv_reader:
        try:
            start_date = date.fromisoformat(row['start_date'])
            end_date = date.fromisoformat(row['end_date'])
            website = row['website']
            description = row['description']
        except (KeyError, ValueError) as exc:
            raise MalformedCSV from exc

        event = Event(
            start_date=start_date,
            end_date=end_date,
            website=website,
            description=description
        )

        results.add(event)

    return results


def plan_changes(calendar_id: int, existing_events: Dict[Event, int], desired_events: Set[Event]) -> Plan:
    """
    Compare the old and new events and work out what changes to make
    against the API
    """
    existing_event_set = set(existing_events.keys())
    events_to_remove = existing_event_set - desired_events
    events_to_add = desired_events - existing_event_set

    ids_to_remove = {existing_events[event_id] for event_id in events_to_remove}

    return Plan(
        calendar_id=calendar_id,
        to_remove=ids_to_remove,
        to_add=events_to_add
    )