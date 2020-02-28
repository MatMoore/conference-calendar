from typing import Set
from datetime import date
from csv import DictReader
from models import Event

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