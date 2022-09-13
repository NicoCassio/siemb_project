from __future__ import print_function

import os.path
import logging
import sys
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def handle_unhandled_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical('Unhandled exception', exc_info=(exc_type, exc_value, exc_traceback))
    logging.info('END')

def get_data():
    START_TIME = time.perf_counter()

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    SPREADSHEET_ID = '1OGCXrcHVBvbct4GgMQx1DY7aP2UIquCo0zOZ-zJSs8Q'
    RANGE_NAME = 'user_codes'

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    end_time = time.perf_counter()
    elapsed_time = end_time - START_TIME
    logging.info(f'API authenticated ({elapsed_time})')

    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()

        end_time = time.perf_counter()
        elapsed_time = end_time - START_TIME
        logging.info(f'Request sent ({elapsed_time})')

        values = result.get('values', [])

        if values:
            gs_data = {
                'names': [],
                'codes': []
            }

            for i, value in enumerate(values):
                if i == 0:
                    continue

                gs_name = value[0].lower()

                gs_data['names'].append(gs_name)
                gs_data['codes'].append(value[1])

            return gs_data
    except HttpError as err:
        logging.exception('Error during request')

def main():
    now   = time.localtime()
    year  = now.tm_year
    month = now.tm_mon
    day   = now.tm_mday

    logging.basicConfig(filename=f'logs/{year}_{month}_{day}_gs.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - [%(levelname)s] %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    sys.excepthook = handle_unhandled_exceptions

    logging.info('START')

    print(get_data())


if __name__ == '__main__':
    main()
