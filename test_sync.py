from sync import parse_events, plan_changes, Event, MalformedCSV
from pathlib import Path
from datetime import date
import pytest


def test_parsing_valid_events():
    with open(Path('test_data', '2020.csv')) as csv_file:
        events = parse_events(csv_file)

    expected_events = set((
        Event(
            start_date=date(2020, 3, 1),
            end_date=date(2020, 3, 2),
            website='https://www.google.com',
            description='test conference'
        ),
        Event(
            start_date=date(2020, 3, 2),
            end_date=date(2020, 3, 4),
            website='https://www.google.com',
            description='another test conference'
        ),
    ))

    assert events == expected_events


def test_parsing_valid_events():
    with open(Path('test_data', 'empty.csv')) as csv_file:
        events = parse_events(csv_file)

    assert events == set()


@pytest.mark.parametrize("filename", ['invalid_date.csv', 'missing_header.csv'])
def test_malformed_csv(filename):
    with open(Path('test_data', filename)) as csv_file:
        with pytest.raises(MalformedCSV):
            events = parse_events(csv_file)


def test_edit_event():
    original_event = Event(
        start_date=date(2020, 3, 2),
        end_date=date(2020, 3, 4),
        website='https://www.google.com',
        description='another test conference'
    )

    changed_event = Event(
        start_date=date(2020, 3, 2),
        end_date=date(2020, 3, 4),
        website='https://www.google.com',
        description='updated description'
    )

    unchanged_event = Event(
        start_date=date(2020, 3, 1),
        end_date=date(2020, 3, 2),
        website='https://www.google.com',
        description='test conference'
    )

    old_events = set((
        unchanged_event,
        original_event,
    ))

    new_events = set((
        unchanged_event,
        changed_event
    ))

    plan = plan_changes(old_events, new_events)

    assert plan.to_add == set((changed_event,))
    assert plan.to_remove == set((original_event,))


def test_nothing_to_change():
    events = set((
        Event(
            start_date=date(2020, 3, 1),
            end_date=date(2020, 3, 2),
            website='https://www.google.com',
            description='test conference'
        ),
        Event(
            start_date=date(2020, 3, 2),
            end_date=date(2020, 3, 4),
            website='https://www.google.com',
            description='another test conference'
        )
    ))

    plan = plan_changes(events, events)

    assert plan.to_add == set()
    assert plan.to_remove == set()