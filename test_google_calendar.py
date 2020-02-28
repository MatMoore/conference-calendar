from google_calendar import parse_event_body, build_event_body
from datetime import date
from models import Event


def test_parse():
    response = {
        'start': {
            'date': '2000-01-01',
        },
        'end': {
            'date': '2000-01-01',
        },
        'extendedProperties': {
            'shared': {
                'website': 'https://google.com',
            }
        },
        'description': 'foo\n\n<a href="https://google.com">https://google.com</a>',
        'summary': 'test',
    }

    actual = parse_event_body(response)

    expected = Event(
        start_date=date(2000, 1, 1),
        end_date=date(2000, 1, 1),
        website='https://google.com',
        description='foo',
        title='test'
    )

    assert actual == expected


def test_build():
    event = Event(
        start_date=date(2000, 1, 1),
        end_date=date(2000, 1, 1),
        website='https://google.com',
        description='foo',
        title='test'
    )

    actual = build_event_body(event)

    expected = {
        'start': {
            'date': '2000-01-01',
        },
        'end': {
            'date': '2000-01-01',
        },
        'extendedProperties': {
            'shared': {
                'website': 'https://google.com',
            }
        },
        'description': 'foo\n\n<a href="https://google.com">https://google.com</a>',
        'summary': 'test',
    }

    assert actual == expected


def test_build_multiday():
    """
    The end date in the API is the following day, not the last day of the conference
    https://developers.google.com/calendar/v3/reference/events/insert
    """
    event = Event(
        start_date=date(2000, 1, 1),
        end_date=date(2000, 1, 2),
        website='https://google.com',
        description='foo',
        title='test'
    )

    actual = build_event_body(event)

    expected = {
        'start': {
            'date': '2000-01-01',
        },
        'end': {
            'date': '2000-01-03',
        },
        'extendedProperties': {
            'shared': {
                'website': 'https://google.com',
            }
        },
        'description': 'foo\n\n<a href="https://google.com">https://google.com</a>',
        'summary': 'test',
    }

    assert actual == expected


def test_build_multiday_on_month_boundary():
    """
    The end date in the API is the following day, not the last day of the conference
    https://developers.google.com/calendar/v3/reference/events/insert
    """
    event = Event(
        start_date=date(2000, 12, 30),
        end_date=date(2000, 12, 31),
        website='https://google.com',
        description='the conference where we discuss dodgy datetime arithmetic',
        title='new years eve conf'
    )

    actual = build_event_body(event)

    expected = {
        'start': {
            'date': '2000-12-30',
        },
        'end': {
            'date': '2001-01-01',
        },
        'extendedProperties': {
            'shared': {
                'website': 'https://google.com',
            }
        },
        'description': 'the conference where we discuss dodgy datetime arithmetic\n\n<a href="https://google.com">https://google.com</a>',
        'summary': 'new years eve conf',
    }

    assert actual == expected


def test_parse_multiday():
    response = {
        'start': {
            'date': '2000-01-01',
        },
        'end': {
            'date': '2000-01-03',
        },
        'extendedProperties': {
            'shared': {
                'website': 'https://google.com',
            }
        },
        'description': 'foo\n\n<a href="https://google.com">https://google.com</a>',
        'summary': 'test',
    }

    actual = parse_event_body(response)

    expected = Event(
        start_date=date(2000, 1, 1),
        end_date=date(2000, 1, 2),
        website='https://google.com',
        description='foo',
        title='test'
    )

    assert actual == expected


def test_parse_single_day_with_weird_end_date():
    """
    If the end date is 1 day after the start date, I think
    it's still supposed to be a single day event.

    https://developers.google.com/calendar/v3/reference/events/insert
    """
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
        'description': 'foo\n\n<a href="https://google.com">https://google.com</a>',
        'summary': 'test',
    }

    actual = parse_event_body(response)

    expected = Event(
        start_date=date(2000, 1, 1),
        end_date=date(2000, 1, 1),
        website='https://google.com',
        description='foo',
        title='test'
    )

    assert actual == expected