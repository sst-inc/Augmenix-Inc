import os.path
import members.members_main
import progressbadges.prog_main
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
SHARED_DRIVE_ID = "0ANi9utLqR454Uk9PVA"
MAIN_TABLE_ID = "1v9ItNHslIZbQCRPdur5u30ITOvj-QXzrAXlZMjNEpLA"
PROG_BADGES_FOLDER_ID = "1Rotyfkp-afJPPIXvJGmnFfCXMDsjql6f"
PROG_BADGES_RC_FOLDER_ID = "1cVq9258U5P-cF7g9BG54-XSVZ0FeEnHN"
PROG_BADGES_TEMPLATE_ID = "1VBel6UvayBjrKENMPX1B32KGHklAi-ZwShOcgDoFTUY"
drive_service = None
sheets_service = None
main_table = []


def get_file_id(url: str):
    path = urlparse(url).path
    path_segments = PurePosixPath(unquote(path)).parts
    file_id = path_segments[3]
    return file_id


def get_csv(url: str):
    global drive_service

    file_id = get_file_id(url)

    # Call the Drive v3 API
    file_result = drive_service.files().export(
        fileId=file_id, mimeType="text/csv")
    csvStr: str = file_result.execute().decode("utf-8")

    return csvStr


def get_csv_table(url: str, include_headers: bool):
    csvStr = get_csv(url)

    rows = csvStr.split("\r\n")
    for each_row_str in rows:
        if each_row_str == "":
            rows.remove(each_row_str)
    num_rows = len(rows)
    if num_rows == 0:
        return []
    cols_0 = rows[0].split(",")
    num_cols = len(cols_0)
    if num_cols == 0:
        return []

    table = []
    start_index = 0 if include_headers else 1
    for i in range(start_index, num_rows):
        cols = rows[i].split(",")
        for j in range(num_cols):
            if i == start_index:
                table.append([cols[j].replace("\;", ",")])
                continue
            table[j].append(cols[j].replace("\;", ","))

    return table


def conv_table_csv(table: list):
    num_cols = len(table)
    if num_cols == 0:
        return ""
    num_rows = len(table[0])
    csv_str = ""
    for i in range(num_rows):
        col_str = ""
        for j in range(num_cols):
            element = table[j][i]
            col_str += element + ","
        col_str = col_str.rstrip(",")
        col_str += "\n"
        csv_str += col_str
    csv_str = csv_str.rstrip("\n")
    return csv_str


def validate_choice_input(choice: str, max: int):
    if choice == "b":
        return True
    if not choice.isdigit():
        return False
    return 1 <= int(choice) <= max


def init():
    global drive_service, sheets_service, main_table

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        print("Downloading required data...")
        main_table = get_csv_table(
            f"https://docs.google.com/spreadsheets/d/{MAIN_TABLE_ID}/edit?usp=sharing", include_headers=True)
        return True
    except HttpError as error:
        print(f'An error occurred: {error}')
        return False


def get_first_user_input():
    print(
        """
Welcome to Stacked Admin Console (Python), select an action:
1. Manage members
2. Manage progress badges
3. Manage event badges (coming soon)
4. Manage unit achievements (coming soon)
b. Go back (exit program)
""")
    choice = input("Your choice (1-4, b): ")
    while not validate_choice_input(choice, 4):
        choice = input("Invalid input. Re-enter your choice (1-4): ")
    if choice == "1":
        members.members_main.get_members_user_input()
    elif choice == "2":
        progressbadges.prog_main.get_prog_user_input()
