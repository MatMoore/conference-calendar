from sync import (
    parse_events, plan_changes,
    Event, MalformedCSV, Plan,
    Syncer
)
from pathlib import Path
from datetime import date
import pytest
from unittest.mock import Mock


def test_parsing_valid_events():
    with open(Path('test_data', '2020.csv')) as csv_file:
        events = parse_events(csv_file)

    expected_events = set((
        Event(
            title='expected1',
            start_date=date(2020, 3, 1),
            end_date=date(2020, 3, 2),
            website='https://www.google.com',
            description='test conference'
        ),
        Event(
            title='expected2',
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
        title='original',
        start_date=date(2020, 3, 2),
        end_date=date(2020, 3, 4),
        website='https://www.google.com',
        description='another test conference'
    )

    changed_event = Event(
        title='changed',
        start_date=date(2020, 3, 2),
        end_date=date(2020, 3, 4),
        website='https://www.google.com',
        description='updated description'
    )

    unchanged_event = Event(
        title='unchanged',
        start_date=date(2020, 3, 1),
        end_date=date(2020, 3, 2),
        website='https://www.google.com',
        description='test conference'
    )

    existing_events = {
        unchanged_event: 1,
        original_event: 2,
    }

    desired_events = set((
        unchanged_event,
        changed_event
    ))

    plan = plan_changes(
        calendar_id=123,
        existing_events=existing_events,
        desired_events=desired_events
    )

    assert plan.to_add == set((changed_event,))
    assert plan.to_remove == set((2,))


def test_nothing_to_change():
    event1 = Event(
        title='event1',
        start_date=date(2020, 3, 1),
        end_date=date(2020, 3, 2),
        website='https://www.google.com',
        description='test conference'
    )
    event2 = Event(
        title='event2',
        start_date=date(2020, 3, 2),
        end_date=date(2020, 3, 4),
        website='https://www.google.com',
        description='another test conference'
    )
    events = set((
        event1,

    ))

    plan = plan_changes(
        calendar_id=123,
        existing_events={
            event1: 1,
            event2: 2
        },
        desired_events=set((event1, event2))
    )

    assert plan.to_add == set()
    assert plan.to_remove == set()


def test_syncer_obeys_the_plan():
    changed_event = Event(
        title='changed',
        start_date=date(2020, 3, 2),
        end_date=date(2020, 3, 4),
        website='https://www.google.com',
        description='updated description'
    )

    removed_event_id = 123

    plan = Plan(
        calendar_id=1234,
        to_add=set((changed_event,)),
        to_remove=set((removed_event_id,))
    )

    calendar_api = Mock()
    csv_parser = Mock()
    planner = Mock()

    calendar_api.add = Mock()
    calendar_api.remove = Mock()
    planner.plan = Mock(return_value=plan)

    syncer = Syncer(calendar_api, csv_parser, planner)
    syncer.sync()

    calendar_api.add.assert_called_once_with(changed_event)
    calendar_api.remove.assert_called_once_with(removed_event_id)