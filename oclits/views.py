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
    # USER HAS LOGGED IN
    if request.method == "POST":
        if 'user' in request.POST:
            user_id = request.POST.get('user')
            password = request.POST.get('password')
            user = authenticate(username=user_id, password=password)
            #print(user)
            if user: 
                data = sheets.fetch_data(user_id)
                task_list = data[0]
                userid = data[1]
                #print(task_list)
                #datetime = sheets.get_datetime()
                return render(request, 'oclits/tasksubmission.html', context={'task_list' : task_list, 'userid': userid, 'datetime' : datetime})
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
            print(request.POST)
            userid = data[1]
            timeticketdate = data[2]
            intime = data[3]
            outtime = data[4]
            print(data)
            data.pop(0) # remove csrf token list
            data.pop(0) # remove userd from list
            data.pop(0) # remove intime
            data.pop(0) # remove outtime
            data.pop(0) # remove date
            data.pop()# remove submit button data
            print(data)
            #print(request)
            _data = list()
            for i in range(0, len(data), 2):
                _data.append(
                    [data[i], data[i+1] ])
            print(_data)
            sheets.write_interns_data(userid, _data, timeticketdate, intime, outtime)
            
            return render(request, 'oclits/login.html') 
            #else:
            #    return HttpResponse("You have already submitted date")
        # SHOW LOGIN PAGE
    else:
        return render(request, 'oclits/login.html')
