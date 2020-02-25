# UK Software Engineering Events Calendar
A CSV dataset of software engineering conferences that can be imported into a calendar.

## How to use
- [View the calendar](https://calendar.google.com/calendar/embed?src=dtevk4lr2i35d9gri6v7lrijtc%40group.calendar.google.com&ctz=Europe%2FLondon)
- [Download in iCal format](https://calendar.google.com/calendar/ical/dtevk4lr2i35d9gri6v7lrijtc%40group.calendar.google.com/public/basic.ics)

## How to add events
1. [Edit the CSV file](https://github.com/MatMoore/conference-calendar/edit/master/data/2020.csv)
2. Commit the changes to a new branch and open a pull request

## How to setup for local development or fork this project

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
