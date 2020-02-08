"""
Load events from CSV
Load events from Calendar
Calculate Removals, Additions
Execute
"""
from typing import NamedTuple, List
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


class MalformedCSV(Exception):
    """
    Raised if the input CSV is malformed.
    """


def parse_events(csv_file) -> List[Event]:
    """
    Parse a CSV file and return a list of events
    """
    results = []
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

        results.append(event)

    return results