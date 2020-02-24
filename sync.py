"""
Load events from CSV
Load events from Calendar
Calculate Removals, Additions
Execute
"""
from typing import NamedTuple, Set, Dict, Optional
from datetime import date
from csv import DictReader
from httplib2 import Http
import ast
import os
import datetime
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


HEADER_NAMES = ['start_date', 'end_date', 'website', 'description']


class Event(NamedTuple):
    """
    A calendar entry for a conference

    TODO: add event title
    """
    start_date: date
    end_date: date
    website: Optional[str]
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


class CalendarAPI:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    CALENDAR_ID = os.environ['CALENDAR_ID']

    def __init__(self):
        client_secret_dict = ast.literal_eval(os.environ['CLIENT_SECRET_JSON'])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            client_secret_dict, scopes=self.SCOPES)
        http = credentials.authorize(Http())
        self.calendar = build('calendar', 'v3', http=http)

    def _parse_event(self, event):
        start_date = date.fromisoformat(event['start']['date'])
        end_date = date.fromisoformat(event['end']['date'])

        try:
            website = event['extendedProperties']['shared']['website']
        except KeyError:
            website = None

        description = event['description']

        return Event(
            start_date = start_date,
            end_date = end_date,
            website = website,
            description = description
        )

    def fetch_events(self) -> Dict[Event, int]:
        """
        Fetch events from the remote calendar.
        Returns a dictionary where the key is the event details and the value is the event ID

        See https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html#list
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        request = self.calendar.events().list(
            calendarId=self.CALENDAR_ID,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        )
        events_result = request.execute()
        raw_events = events_result.get('items', [])

        events = {}

        for raw_event in raw_events:
            event_id = raw_event['id']
            event = self._parse_event(raw_event)
            events[event] = event_id

        return events


if __name__ == '__main__':
    api = CalendarAPI()
    api.fetch_events()