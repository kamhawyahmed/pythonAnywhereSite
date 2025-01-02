import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path #pythonanywhere compatibility - convert relative to abs path


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def create_event(event_name, startDateTime, endDateTime, colorId):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      THIS_FOLDER = Path(__file__).parent.resolve()
      absolute_file_path = THIS_FOLDER / "credentials.json"
      flow = InstalledAppFlow.from_client_secrets_file(
          absolute_file_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    EVENT = {
        "summary": event_name,
        # "start": {"dateTime":"2023-11-25T11:00:00-05:00"},
        "start": {"dateTime": startDateTime, "timeZone":"EST"},
        "end": {"dateTime": endDateTime, "timeZone":"EST"},
        "colorId": colorId
    }
    if EVENT["colorId"] == "invalid":
        EVENT.pop('colorId', None)

    event_object = service.events().insert(calendarId="09b244fd57d4f16dc6d12a67a730c003742343e55ebe4ccff407b6692ea5aa10@group.calendar.google.com", sendNotifications=False, body=EVENT).execute()
    return event_object

  except HttpError as error:
    print(f"An error occurred: {error}")



if __name__ == "__main__":
  create_event(event_name="Sleep (Ahmed's Watch)", startDateTime="2025-01-02T00:00:04", endDateTime="2025-01-02T00:57:34", colorId=10)