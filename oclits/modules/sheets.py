import re
from googleapiclient.discovery import build
from collections import Counter
from google.oauth2 import service_account
import os
import datetime
import cryptocode
#from ..models import UserLogs
# parent directory of the directory where program resides.
DIRNAME = os.path.dirname(__file__)
SERVICE_ACCOUNT_FILE = os.path.join(DIRNAME,'cre.json')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
  SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1VhQVUY34zKhYYPrSXE485R6W36XVIfs6I0v-h0pARN4'

service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()
current_month = datetime.datetime.today().strftime("%b")


def time_ticket_data(userid):

    table = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                              range= userid + ' attendance' + "!A2:C").execute()['values']
    user_tasks = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range= "MasterTaskSheet!A2:C").execute()['values']
    task_data = list()
    for task in user_tasks:
        if task[1]==userid:
            task_data.append(task)
    return table, task_data

def duplicate_sheet(sheet_name):
    sheet_name = sheet_name + current_month
    request = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    available_sheets = list()
    for each_sheet in request['sheets']:
        available_sheets.append(each_sheet['properties']['title'])
    if sheet_name in available_sheets:
        return 'sheet has already been duplicated'
    else:
        body = {
            'requests': [{
                'duplicateSheet': {
                    'sourceSheetId': 0,
                    #'insertSheetIndex': 1,
                    'newSheetName': sheet_name,
                    #"newSheetId":
                }
            }]
        }
        result = sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                body=body).execute()
        return 'sheet has been duplicated'

"""
def copy_data(sheet_name):

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='Tasks' + "!A:Q").execute()
    data = result['values']
    for i in range(3, len(data)):
        if data[i][3] == sheet_name:
            sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                  range=sheet_name + "!A:Q",
                                  valueInputOption="USER_ENTERED",
                                  body={
                                      "values": [data[i]]
                                  }).execute()
"""


def add_sheets(sheet_name):
    sheet_name = sheet_name + current_month
    request = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    available_sheets = list()
    for each_sheet in request['sheets']:
        available_sheets.append(each_sheet['properties']['title'])
    if sheet_name in available_sheets:
        #copy_data(sheet_name)
        return True
    else:
        try:
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name,
                            'tabColor': {
                                'red': 0.44,
                                'green': 0.99,
                                'blue': 0.50
                            }
                        }
                    }
                }]
            }

            sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                        body=request_body).execute()
            return 'executed successfully'
        except Exception as e:
            return e

def fetch_data(user):
    result = sheet.values().get(spreadsheetId = SPREADSHEET_ID,range= "MasterTaskSheet!A:F").execute()
    #print(result)
    data = {}
    for i in range(len(result['values'])):
        data['task' + str(i+1)] = result['values'][i][0]
    #data['userid'] = user
    return data, user

def update(date, data):
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="MasterTaskSheet!A2:G").execute()['values']
    for i in range(len(result)):
        if result[i][0] == date:
            print(date)
            print(i)
            sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                range="MasterTaskSheet!"+"D"+str(i+2)+":G",
                                valueInputOption="USER_ENTERED",
                                body={
                                    "values": data
                                }).execute()


def fetch_data_for_visualization(user):
    tasks = sheet.values().get(spreadsheetId = SPREADSHEET_ID,range= user+"!A:B").execute()
    frequency = sheet.values().get(spreadsheetId= SPREADSHEET_ID, range = user+'!A2:A').execute()
    #print(result)
    data = {}
    for i in range(1, len(tasks['values'])):
        data[tasks['values'][i][0]] = int(0)

    for i in range(1, len(tasks['values'])):
        data[tasks['values'][i][0]] = data[tasks['values'][i][0]]+int(tasks['values'][i][1])

    task_list =list( data.keys())
    task_frqeuency = list(data.values())
    #print(task_list)
    #print(task_frqeuency)
    return task_list, task_frqeuency
#print(fetch_data_for_visualization('hadi'))
"""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=user+"!A2:A").execute()
    data = list()
    #print(result['values'])
    for  value in result['values']:
        data.append(value[0])
    task = list()
    task_frequency = list()
    data_counter = Counter(data).most_common()
    print(data_counter)
    for each_task in data_counter:
        task.append(each_task[0])
        task_frequency.append(each_task[1])
    return task, task_frequency
    """
"""
def get_data(user):
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="HadiTasks!A2:").execute()
"""
def authenticate_from_sheets(user, password):
    result = sheet.values().get(spreadsheetId = SPREADSHEET_ID,range= "users!A2:B2").execute()
    users = result['values']
    for credentials in users:
        if credentials[0] == user and cryptocode.decrypt(credentials[1], user) == password:
            return True
    else:
        return False
#if user[0] == 'hadi':

def write_interns_data(user, data, date, intime, outtime):
    sheet.values().append(spreadsheetId=SPREADSHEET_ID,range=user+"!A2:A", valueInputOption = "USER_ENTERED", body = {"values" : data}).execute()
    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=user+"!C2:C",
                          valueInputOption="USER_ENTERED", body={"values": [[intime]]}).execute()

    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=user+"!D2:D",
                          valueInputOption="USER_ENTERED", body={"values": [[outtime]]}).execute()

    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=user+"!E2:E",
                          valueInputOption="USER_ENTERED", body={"values": [[date]]}).execute()
    #log = UserLogs(user = user, login_time = datetime.date.today())
    #log.save()

"""
def validate_login(userid):
    if UserLogs.objects.filter(user = userid, login_time = datetime.date.today()):
        return False
    else:
        return True

"""
