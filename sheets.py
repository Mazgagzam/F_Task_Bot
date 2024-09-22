from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = './service.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)


SPREADSHEET_ID = "1PqrboTQuTrW2295LhlaWjHD69fbKVWHlKNi9udl60n0"
api_key = "AIzaSyBisHmOLjCEjd8vXVjmKdQ0zlolNa6rMtE"
RANGE_NAME = 'heet!A10'



async def append_line(values):
    body = {
        'values': [values]
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result
