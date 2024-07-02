from __future__ import print_function

import datetime
import time
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarAPI():
    def __init__(self):
        self.creds = None
        self.authorization_setup()
    def authorization_setup(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

#TODO switch to EST time 00:00 - may be hard
    def get_events(self, start_date='01/02/23', end_date="04/02/24"):
        # date not exact start on date end on day after for one day extraction
        # timemax sets datetime that any events that start after will not be included
        # -  current setup means time works in UTC time 00:00 which is 7pm EST
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            # Call the Calendar API
            # date_object = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            # START_DATE = '01/05/23' #12am in utc time
            start_date_formatted = datetime.datetime.strptime(start_date, '%d/%m/%y').isoformat() + 'Z'
            end_date_formatted = datetime.datetime.strptime(end_date, '%d/%m/%y').isoformat() + 'Z'
            print(f'Getting events from {start_date} to {end_date}.')
            events_result = service.events().list(calendarId='2f5923e533d4aa08563c7cfda4401cb38950d1e4a3adf5b84b99f5cbefc59f89@group.calendar.google.com', timeMin=start_date_formatted,
                                                       timeMax= end_date_formatted,
                                                       maxResults=10000, singleEvents=True,
                                                       orderBy='startTime').execute()

            with open("data.json", "w") as file:
                json.dump(events_result, file, indent=4)

            events = events_result.get('items', [])
            if not events:
                print('No upcoming events found.')
                return
            return events_result

        except HttpError as error:
            print('An error occurred: %s' % error)

    def start_calendar(self):
        service = build('calendar', 'v3', credentials=self.creds)
        return service

    def get_events_details_for_app(self, start_date='01/02/23'):
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            # Call the Calendar API
            # date_object = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            # start_date = '16/06/23' #12am in utc time
            date_formatted = datetime.datetime.strptime(start_date, '%d/%m/%y').isoformat() + 'Z'
            print('Getting all events from start time')
            events_result = service.events().list(calendarId='2f5923e533d4aa08563c7cfda4401cb38950d1e4a3adf5b84b99f5cbefc59f89@group.calendar.google.com', timeMin=date_formatted,
                                                       maxResults=10000, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])
            with open("app_data.json", "w") as file:
                json.dump(events_result, file, indent=4)

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                colorid = event.get("colorId", "No colour id.") #only set when non-default colour and NOT group event - BUT CAN PATCH IT IN FOR GROUP EVENTS STILL
                name = event['summary']
                status = event['status']
                attendees = event.get('attendees', "Not group event.") #list of dictionaries - known by email key or self key = true to be self, access responseStatus key

                print(start, end, name, colorid, status, attendees)


        except HttpError as error:
            print('An error occurred: %s' % error)

#TODO cycle through events looking for contain specific names - make count of events matching and collect name start end color

    def change_color(self, eventId, calendarId="2f5923e533d4aa08563c7cfda4401cb38950d1e4a3adf5b84b99f5cbefc59f89@group.calendar.google.com"):

        try:
            service = build('calendar', 'v3', credentials=self.creds)
            changed_event = service.events().patch(calendarId=calendarId, eventId=eventId, body={"colorId": None}).execute() #colorid 5 = yellow
        except HttpError as error:
            print('An error occurred: %s' % error)
    def confirm_going_event(self, eventId, calendarId="primary"):
        """primary calendar only"""

        try:
            service = build('calendar', 'v3', credentials=self.creds)
            changed_event = service.events().patch(calendarId=calendarId, eventId=eventId, body={"attendees": [
                {
                    "email": "kamhawyalif@gmail.com",
                    "self": "true",
                    "responseStatus": "accepted"
                }
            ],}).execute() #colorid 5 = yellow
        except HttpError as error:
            print('An error occurred: %s' % error)
    def get_calendar_list(self):
        service = build('calendar', 'v3', credentials=self.creds)

        # Call the Calendar API
        print('Getting list of calendars')
        calendars_result = service.calendarList().list().execute()

        calendars = calendars_result.get('items', [])

        if not calendars:
           print('No calendars found.')
        for calendar in calendars:
           summary = calendar['summary']
           id = calendar['id']
           primary = "Primary" if calendar.get('primary') else ""
           print("%s\t%s\t%s" % (summary, id, primary))


    def update_color_status_current_month_shifts(self):
        # buggy on last day of month
        service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.datetime.now()
        # start_date =
        # end_date =
        # events_result = self.get_events(start_date=,end_date=)
        events_result = self.get_events()
        events = events_result.get('items', [])
        print("Changing event status and color.")
        for event in events:
            if "SLER" in event.get("summary", "No Title"):
                self.change_color(eventId=event['id'])
                self.confirm_going_event(eventId=event['id'])

    def update_color_status_selected_events(self, events_result_to_be_color_changed):
        service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.datetime.now()
        # start_date =
        # end_date =
        # events_result = self.get_events(start_date=,end_date=)
        events = events_result_to_be_color_changed.get('items', [])
        for event in events:
            self.change_color(eventId=event['id'])

    def create_event(self, colorId = "invalid", event_name="Sleep Test", startDateTime="2023-11-25T11:00:00", endDateTime="2023-11-25T13:00:00-05:00", ):
        service = self.start_calendar()
        EVENT = {
            "summary": event_name,
            # "start": {"dateTime":"2023-11-25T11:00:00-05:00"},
            "start": {"dateTime": startDateTime, "timeZone":"EST"},
            "end": {"dateTime": endDateTime, "timeZone":"EST"},
            "colorId": colorId
        }
        if EVENT["colorId"] == "invalid":
            EVENT.pop('colorId', None)

        event_object = service.events().insert(calendarId="c61764f38171d3c2c736b09d5c9e1fe517271f584d500aad7ee837fac6baa457@group.calendar.google.com", sendNotifications=False, body=EVENT).execute()
        return event_object

    def check_duplicate_event(self):

        return

    def delete_event(self, event):
        service = self.start_calendar()
        service.events().delete(calendarId="primary", eventId=event["id"]).execute()
        return





if __name__ == '__main__':
    API = GoogleCalendarAPI()
    print(API.get_events())
    # API.get_events_details_for_app()
    API.change_color(eventId="46pv2cdcj316h2n6g60sqt2100")
    # API.confirm_going_event(eventId="aq7dichdv7iih779ejkhejn2sg")
    # API.get_calendar_list()
    # API.update_color_status_current_month_shifts()
    # new_event = API.create_event()
    print("new event created")
    # time.sleep(10)
    # print("deleting")
    # API.delete_event(new_event)

