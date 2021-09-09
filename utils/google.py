# TODO: replace print statements with logging.info 
import os
from google.auth.environment_vars import CREDENTIALS
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .util import convert_to_RFC_datetime


COLOUR_ID = 5


def create_service(client_secret_file, api_name, api_version, *scopes): 
    """ Connect to a specific Google API """
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    cred = None
    print(os.getcwd())

    if os.path.exists('token.json'):
        cred = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(cred.to_json())
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        return None


def create_event(start_hour, stop_hour):
    """ Make calendar event """
    start_hour = convert_to_RFC_datetime(start_hour)
    stop_hour = convert_to_RFC_datetime(stop_hour)

    # TODO: Update the quote each time

    event = {
        'summary': 'Gym',
        'description': 'Strength does not come from winning. Your struggles develop your strengths. When you go through hardships and decide not to surrender, that is strength. - Arnold Schwarzenegger',
        'start': {
            'dateTime': start_hour,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': stop_hour,
            'timeZone': 'America/New_York',
        },
        'location': '175 Longwood Rd S Suite 101A, Hamilton, ON L8P 0A1',
        'colorId' : COLOUR_ID,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes':24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    
    return event