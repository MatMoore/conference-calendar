"""
Load events from CSV
Load events from Calendar
Calculate Removals, Additions
Execute
"""
from typing import Set, Dict
from datetime import date
from csv import DictReader
from models import Event, Plan
from google_calendar import CalendarAPI

HEADER_NAMES = ['start_date', 'end_date', 'title', 'website', 'description']


class MalformedCSV(Exception):
    """
    Raised if the input CSV is malformed.
    """


def parse_events(csv_file):
    return CsvParser(csv_file).parse_events()


class CsvParser:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def parse_events(self) -> Set[Event]:
        """
        Parse a CSV file and return a list of events
        """
        results = set()
        csv_reader = DictReader(self.csv_file)

        if csv_reader.fieldnames != HEADER_NAMES:
            raise MalformedCSV(f'Expected header to equal {HEADER_NAMES} but got {csv_reader.fieldnames}')

        for row in csv_reader:
            try:
                start_date = date.fromisoformat(row['start_date'])
                end_date = date.fromisoformat(row['end_date'])
                website = row['website']
                description = row['description']
                title = row['title']
            except (KeyError, ValueError) as exc:
                raise MalformedCSV from exc

            event = Event(
                start_date=start_date,
                end_date=end_date,
                website=website,
                description=description,
                title=title
            )

            results.add(event)

        return results


def plan_changes(calendar_id: int, existing_events: Dict[Event, int], desired_events: Set[Event]) -> Plan:
    """
    Compare the old and new events and work out what changes to make
    against the API
    """
    return Planner(calendar_id).plan(existing_events, desired_events)


class Planner:
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id

    def plan(self, existing_events: Dict[Event, int], desired_events: Set[Event]) -> Plan:
        existing_event_set = set(existing_events.keys())
        events_to_remove = existing_event_set - desired_events
        events_to_add = desired_events - existing_event_set

        ids_to_remove = {existing_events[event_id] for event_id in events_to_remove}

        return Plan(
            calendar_id=self.calendar_id,
            to_remove=ids_to_remove,
            to_add=events_to_add
        )


class Syncer:
    def __init__(self, calendar_api, csv_parser, planner):
        self.calendar_api = calendar_api
        self.csv_parser = csv_parser
        self.planner = planner

    def sync(self):
        existing_events = self.calendar_api.fetch_events()
        desired_events = self.csv_parser.parse_events()
        plan = self.planner.plan(existing_events, desired_events)

        for event_id in plan.to_remove:
            self.calendar_api.remove(event_id)

        for event in plan.to_add:
            self.calendar_api.add(event)


def sync(filename):
    api = CalendarAPI()
    planner = Planner(api.CALENDAR_ID)

    with open(filename) as csv_file:
        parser = CsvParser(csv_file)
        Syncer(api, parser, planner).sync()


if __name__ == '__main__':
    sync('data/2020.csv')