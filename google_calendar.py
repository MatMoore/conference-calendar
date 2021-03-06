from typing import Dict
from datetime import date, datetime, timedelta
from httplib2 import Http
import ast
import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from models import Event


def parse_event_body(event_response) -> Event:
    """
    Parse an event from google calendar
    """
    start_date = date.fromisoformat(event_response['start']['date'])
    end_date = date.fromisoformat(event_response['end']['date'])

    try:
        website = event_response['extendedProperties']['shared']['website']
    except KeyError:
        website = None

    raw_description = event_response['description']
    description, _sep, _website = raw_description.rpartition('\n\n')

    title = event_response['summary']

    if end_date != start_date:
        end_date = end_date + timedelta(days=-1)

    return Event(
        start_date = start_date,
        end_date = end_date,
        website = website,
        description = description,
        title = title
    )


def build_event_body(event: Event):
    """
    Build the body of an event request
    """
    if event.start_date == event.end_date:
        end_date = event.end_date
    else:
        end_date = event.end_date + timedelta(days=1)

    return {
        'summary': event.title,
        'start': {
            'date': event.start_date.isoformat(),
        },
        'end': {
            'date': end_date.isoformat(),
        },
        'description': f'{event.description}\n\n<a href="{event.website}">{event.website}</a>',
        'extendedProperties': {
            'shared': {
                'website': event.website,
            },
        },
    }



class CalendarAPI:
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    def __init__(self):
        self.calendar_id = os.environ['CALENDAR_ID']
        client_secret_dict = ast.literal_eval(os.environ['CLIENT_SECRET_JSON'])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            client_secret_dict, scopes=self.SCOPES)
        http = credentials.authorize(Http())
        self.calendar = build('calendar', 'v3', http=http)

    def remove(self, event_id):
        """
        Remove an event from the calendar
        """
        print(f'removing {event_id}')

        request = self.calendar.events().delete(calendarId=self.calendar_id, eventId=event_id)
        request.execute()

    def add(self, event):
        """
        Add an event to the calendar
        """
        print(f'adding {event}')

        body = build_event_body(event)

        request = self.calendar.events().insert(calendarId=self.calendar_id, body=body)
        request.execute()

    def fetch_events(self) -> Dict[Event, int]:
        """
        Fetch events from the remote calendar.
        Returns a dictionary where the key is the event details and the value is the event ID

        See https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html#list
        """
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        request = self.calendar.events().list(
            calendarId=self.calendar_id,
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
            event = parse_event_body(raw_event)
            events[event] = event_id

        return events