from datetime import date
from models import Event


def parse_event(event_response) -> Event:
    """
    Parse an event from google calendar
    """
    start_date = date.fromisoformat(event_response['start']['date'])
    end_date = date.fromisoformat(event_response['end']['date'])

    try:
        website = event_response['extendedProperties']['shared']['website']
    except KeyError:
        website = None

    description = event_response['description']
    title = event_response['summary']

    return Event(
        start_date = start_date,
        end_date = end_date,
        website = website,
        description = description,
        title = title
    )