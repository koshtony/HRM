from django.shortcuts import render
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse
from django.core import serializers
from .forms import EmpForm,ApprovalForm,LeaveForm,Employee
from .models import *
from datetime import datetime,date
import time
# Create your views here.
@login_required
def home(request):

    return render(request,'management/index.html')

def add_info(request):

    return render(request,'management/add_info.html')

def approvals(request):
    context = {"appForm":ApprovalForm}
    return render(request,'management/approvals.html',context)

def view_approvals(request):

    context = {"processes":Process.objects.filter(applicant=request.user.username)}

    return render(request,'management/approval_list.html',context)

def leave(request):

  
    if request.POST:

        type_ = request.POST.get("type")
 
        category_ = request.POST.get("category")
        start = request.POST.get("start")
        end = request.POST.get("end")
        remarks = request.POST.get("remarks")

        new_leave =  Leave(
             applicant = request.user, Approvals_type = Approvals.objects.get(type=type_),
             category = category_, start=start,end=end,remarks=remarks
        )

        new_leave.save() 

        process = Process(

             applicant = request.user.username ,
             approvals = Approvals.objects.get(type=type_),
             details = str(type_)+"\n"+str(remarks),created = datetime.now(),
             status = "pending"
        )

        process.save()

        todo = Todo(

             recpient_id = Approvals.objects.get(type=type_).approvers.Employee_ids,
             details = str(type_)+": "+str(remarks),
             
        )
        todo.save()

        return JsonResponse("applied successfully",safe=False)
    
   


def add_department(request):

    pass

def add_roles(request):

    pass

def add_employee(request):

    context = {"emp_form":EmpForm()}

    return render(request,'management/add_employees.html',context)

def list_employee(request):

    context = {"employee":Employee.objects.all()}
    
    return render(request,'management/list_employees.html',context)

def get_emp_files(request):

    if request.POST:
        emp_id = request.POST.get("emp_id")
        my_files = EmpFiles.objects.filter(employee=Employee.objects.get(emp_id=emp_id))
        all_my_files = []
        for my_file in my_files:
            file_inst ={
                "category":my_file.category.category_name,
                "file_name":my_file.file_name,
                "document":my_file.document.url,
                "created":my_file.created 
            }
            all_my_files.append(file_inst)
        print(all_my_files)
        return JsonResponse(all_my_files,safe=False)

@login_required
def clock(request):

    context = {'leave_form':LeaveForm(),"approvals":Approvals.objects.all()}
    att_settings =  AttSettings.objects.all()[0]
    if request.POST:

        lat = request.POST.get('latitude')
        long = request.POST.get('longitude')
        image_info = request.POST.get('image_str')
        #print(image_info)
        empty = ""
        att_filt = Attendance.objects.filter(day=date.today()).filter(employee = request.user)
        time_diff = datetime.strptime(datetime.now().strftime("%H:%M:%S"),'%H:%M:%S') -datetime.strptime(att_settings.end.strftime("%H:%M:%S"),"%H:%M:%S")
                                     
        time_diff = time_diff.total_seconds()
        if len(att_filt) == 0 and datetime.now().hour<12: #record initial data
            attendance = Attendance(
                    employee =  request.user,
                    day = date.today(),
                    clock_in = datetime.now(),
                    clock_out = empty,
                    lat =lat ,long=long,image1=image_info,
                    lat1 = empty , long1 = empty, image2 = empty,remarks="clock in"
                    

                )
            attendance.save()
            return JsonResponse("clock in successful",safe=False)
        
        elif len(att_filt)>0 and time_diff >= 0:
            
            att_filt[0].clock_out = datetime.now()
            att_filt[0].lat1 = lat
            att_filt[0].long1 = long 
            att_filt[0].image2 = image_info
            att_filt[0].status = "present"
            att_filt[0].remarks = att_filt[0].remarks+" clock out"
            att_filt[0].save()

            return JsonResponse("clock out successful",safe=False)

        elif len(att_filt) == 0 and time_diff >= 0:
           
            attendance = Attendance(
                    employee =  request.user,
                    day = date.today(),
                    clock_in = "",
                    clock_out = datetime.now(),
                    lat ="" ,long="",image1="",
                    lat1 = lat , long1 = long, image2 = image_info,remarks="clock out"   

                )
            attendance.save()


            return JsonResponse("missed clock in, clocked out",safe=False)

    return render(request,'management/clock.html',context)

def Events(request):

    return render(request,'management/events.html')

def Post(request):

    return render(request,'management/post.html')

