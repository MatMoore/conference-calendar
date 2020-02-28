from datetime import date
from pathlib import Path
from csv_calendar import parse_events, MalformedCSV
from models import Event
import pytest

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
            parse_events(csv_file)
