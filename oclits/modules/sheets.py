import re
from googleapiclient.discovery import build
from collections import Counter
from google.oauth2 import service_account
import os
import datetime
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

def fetch_data(user):
    result = sheet.values().get(spreadsheetId = SPREADSHEET_ID,range= user+"!F2:F").execute()
    #print(result)
    data = {}
    for i in range(len(result['values'])):
        data['task' + str(i+1)] = result['values'][i][0]
    #data['userid'] = user
    return data, user


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

