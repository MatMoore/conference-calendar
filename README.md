# Conference calendar
A CSV dataset of software development conferences, published to a google calendar (WIP).

## Setup

### Create a service user in Google Cloud Platform

1. Create a project
2. Enable google calendar API (under APIs & Services)
3. Create a service user, and note its email address
4. Download the JSON version of the credentials

### Create the calendar

- Check "Make available to public"
- Under "Share with specific people" enter the service user email, and select "Make changes to events"

### Environment variables

- Set CLIENT_SECRET_JSON to the contents of the JSON file you downloaded
- Set CALENDAR_ID to the Calendar ID. The production version is `dtevk4lr2i35d9gri6v7lrijtc@group.calendar.google.com`

## License
[MIT](LICENSE)