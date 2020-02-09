"""
Load events from CSV
Load events from Calendar
Calculate Removals, Additions
Execute
"""
from typing import NamedTuple, List, Set
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
    to_remove: Set[Event]
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


def plan_changes(old_events: Set[Event], new_events: Set[Event]) -> Plan:
    """
    Compare the old and new events and work out what changes to make
    against the API
    """
    to_remove = old_events - new_events
    to_add = new_events - old_events
    return Plan(to_remove=to_remove, to_add=to_add)