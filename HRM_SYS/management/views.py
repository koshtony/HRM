from django.shortcuts import render
from django.http import JsonResponse
from .forms import EmpForm,ApprovalForm,LeaveForm
from datetime import datetime
import time
# Create your views here.
def home(request):

    return render(request,'management/index.html')

def add_info(request):

    return render(request,'management/add_info.html')

def approvals(request):
    context = {"appForm":ApprovalForm}
    return render(request,'management/approvals.html',context)

def view_approvals(request):

    return render(request,'management/approval_list.html')



def add_department(request):

    pass

def add_roles(request):

    pass

def add_employee(request):

    context = {"emp_form":EmpForm()}

    return render(request,'management/add_employees.html',context)

def list_employee(request):
    
    return render(request,'management/list_employees.html')


def clock(request):

    context = {'leave_form':LeaveForm()}

    if request.POST:

        lat = request.POST.get('latitudes')
        long = request.POST.get('longitudes')
        image_info = request.POST.get('image_str')
        #print(image_info)
        t_now= time.localtime()
        current_time = time.strftime("%H", t_now)
        print(current_time)

        return JsonResponse("info submitted",safe=False)

    return render(request,'management/clock.html',context)

def Events(request):

    return render(request,'management/events.html')

def Post(request):

    return render(request,'management/post.html')

