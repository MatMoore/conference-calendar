from google_calendar import parse_event
from datetime import date
from models import Event

def test_parse():
    response = {
        'start': {
            'date': '2000-01-01',
        },
        'end': {
            'date': '2000-01-02',
        },
        'extendedProperties': {
            'shared': {
                'website': 'https://google.com',
            }
        },
        'description': 'foo',
        'summary': 'test',
    }

    actual = parse_event(response)

    expected = Event(
        start_date=date(2000, 1, 1),
        end_date=date(2000, 1, 2),
        website='https://google.com',
        description='foo',
        title='test'
    )

    assert actual == expected