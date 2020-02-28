"""
Update a Google Calendar based on the CSV file
"""
from typing import Set, Dict
from models import Event, Plan
from google_calendar import CalendarAPI
from csv_calendar import CsvParser


def plan_changes(existing_events: Dict[Event, int], desired_events: Set[Event]) -> Plan:
    """
    Compare the old and new events and work out what changes to make
    against the API
    """
    return Planner().plan(existing_events, desired_events)


class Planner:
    def plan(self, existing_events: Dict[Event, int], desired_events: Set[Event]) -> Plan:
        existing_event_set = set(existing_events.keys())
        events_to_remove = existing_event_set - desired_events
        events_to_add = desired_events - existing_event_set

        ids_to_remove = {existing_events[event_id] for event_id in events_to_remove}

        return Plan(
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
    planner = Planner()

    with open(filename) as csv_file:
        parser = CsvParser(csv_file)
        Syncer(api, parser, planner).sync()


if __name__ == '__main__':
    sync('data/2020.csv')