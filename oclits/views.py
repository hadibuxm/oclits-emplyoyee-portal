from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
#from models import UserLogs
from .modules import sheets, dataanalysis
import datetime
# Create your views here.
"""
@login_required
def index(request):
    data = list()
    if request.method == "POST":
        data.append([str(request.POST.get('webdevelopment')), str(request.POST.get("wdhours"))])
        data.append([str(request.POST.get('mobileapplicationdevelopment')), str(request.POST.get("madhours"))])
        print(request.POST)
        print(data)
        sheets.write_interns_data(data)
        #print(request.POST)
        #print(data)
        return render(request, 'oclits/index.html')
    else:
        return render(request, 'oclits/index.html')
"""

def login(request):
    # USER HAS CLICKED LOGIN BUTTON
    if request.method == "POST":
        #print(request.POST)
        #td = request.POST.get()
        if "submittimeticket" in request.POST:
            print(request.POST)
            date = str(request.POST.get("date"))
            data = list()
            data.append(str(request.POST.get('duration')))
            data.append(str(request.POST.get("activity")))
            data.append(str(request.POST.get("progress")))
            data.append(str(request.POST.get("developer_comments")))
            sheets.update(date, [data])
            return HttpResponse("user filled timeticket")

        if 'user' in request.POST:
            user_id = request.POST.get('user') # GET USERNAME   
            password = request.POST.get('password') # GET PASSWORD
            #user = authenticate(username=user_id, password=password) # AUTHENTICATION FROM LOCAL DATABASE
            # PASSWORD AUTHENTICATION
            user = sheets.authenticate_from_sheets(user_id, password)
            #print(user)
            if user:
                #print(request.POST)
                #sheets.add_sheets(user_id)# create sheet if it does not exist
                response = sheets.time_ticket_data(user_id)
                context = {
                    'data' : response[0],
                    'task_data': response[1]
                }
                #print(response[1])
                return render(request, 'oclits/timeticket.html', context)
                #return HttpResponse(sheets.duplicate_sheet(user_id))
                #return HttpResponse(response + ' , data copied')
                """ 
                data = sheets.fetch_data(user_id)
                task_list = data[0]
                userid = data[1]
                return render(request, 'oclits/tasksubmission.html', context={'task_list' : task_list, 'userid': userid, 'datetime' : datetime})
                """
            else:
                return HttpResponse("Wrong Password")

        # USER SUBMITTING DATA
        elif 'showbarchart' in request.POST:
            #print('in showbarchart')
            #print(request.POST)
            chart = dataanalysis.task_barchart(str(request.POST.get('userid')))
            #print(request.POST.get('user'))
            return render(request, 'oclits/visualize.html', {'barchart': chart})
        elif 'submitdata' in request.POST:
            data = list()
            for key, value in request.POST.items():
                data.append(value)
            print(data)
            userid = data[1]
            timeticketdate = data[2]
            intime = data[3]
            outtime = data[4]
            data.pop(0) # remove csrf token list
            data.pop(0) # remove userd from list
            data.pop(0) # remove intime
            data.pop(0) # remove outtime
            data.pop(0) # remove date
            data.pop()# remove submit button data
            _data = list()
            for i in range(0, len(data), 2):
                _data.append(
                    [data[i], data[i+1] ])
            # write data in sheets
            print(_data)
            sheets.write_interns_data(userid, _data, timeticketdate, intime, outtime)

            return render(request, 'oclits/login.html')
            #else:
            #    return HttpResponse("You have already submitted date")
        else:
            return HttpResponse("you forgot to enter username")
        # SHOW LOGIN PAGE
    # SHOW LOGIN PAGE
    else:
        return render(request, 'oclits/login.html')
