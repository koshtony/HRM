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
    att_settings =  AttSettings.objects.filter(employee_id = request.user.username)[0]
    if request.POST:

        lat = request.POST.get('latitude')
        long = request.POST.get('longitude')
        image_info = request.POST.get('image_str')
        #print(image_info)
        empty = ""
        att_filt = Attendance.objects.filter(day=date.today()).filter(employee = Employee.objects.get(emp_id=request.user.username))
        
        early_diff = (datetime.strptime(datetime.now().strftime("%H:%M:%S"),'%H:%M:%S') -datetime.strptime(att_settings.end.strftime("%H:%M:%S"),"%H:%M:%S")).total_seconds()
        '''
             condition to determine if employee  left on time or early; early denoted by -ve
        '''
        if early_diff < 0:

            early_diff = early_diff*-1
        else:
            early_diff = 0
        
        late_diff = (datetime.strptime(datetime.now().strftime("%H:%M:%S"),'%H:%M:%S') - datetime.strptime(att_settings.start.strftime("%H:%M:%S"),"%H:%M:%S")).total_seconds()
        
        if late_diff > 0:

            late_diff =  late_diff 

        else:

            late_diff = 0
                                     
        
        if len(att_filt) == 0: #record initial data
            attendance = Attendance(
                    employee =  Employee.objects.get(emp_id = request.user.username),
                    day = date.today(),
                    clock_in = datetime.now(),
                    clock_out = empty,
                    lat =lat ,long=long,image1=image_info,
                    lat1 = empty , long1 = empty, image2 = empty,remarks="clock in",
                    deductions  = (late_diff/60)*att_settings.deduction_per_minute,

                    

                )
            attendance.save()
            return JsonResponse("clock in successful",safe=False)
        
        elif len(att_filt)>0 and att_filt[0].clock_out == '':
            
            att_filt[0].clock_out = datetime.now()
            att_filt[0].lat1 = lat
            att_filt[0].long1 = long 
            att_filt[0].image2 = image_info
            att_filt[0].status = "present"
            att_filt[0].remarks = att_filt[0].remarks+" clock out"
            att_filt[0].deductions =  att_filt[0].deductions + (early_diff/60)*att_settings.deduction_per_minute
            att_filt[0].save()

            return JsonResponse("clock out successful",safe=False)
        
        elif att_filt[0].clock_in != '' and att_filt[0].clock_out != '':

            return JsonResponse("clock in and clockout already completed",safe=False)


            



    return render(request,'management/clock.html',context)

def get_attendance(request):

    today_att = Attendance.objects.filter(day=date.today()).filter(employee = Employee.objects.get(emp_id=request.user.username))
    att_settings = AttSettings.objects.filter(employee_id = request.user.username)[0]


    if len(today_att) > 0:

        details = {
            "clock_in":today_att[0].clock_in,
            "clock_out":today_att[0].clock_out,
            "h1":att_settings.start.hour,
               "m1":att_settings.start.minute,
            "h2":att_settings.end.hour,
            "m2":att_settings.end.minute,
        }

        return JsonResponse(details,safe=False)
    
    details = {"h1":att_settings.start.hour,
               "m1":att_settings.start.minute,
            "h2":att_settings.end.hour,
            "m2":att_settings.end.minute,
            "clock_in":"",
            "clock_out":"",
        }
    return JsonResponse(details,safe=False)

def upload_leave(request):
    if request.POST:
       
       form = LeaveForm(request.POST,request.FILES)
       if form.is_valid():
            form.instance.applicant = request.user
            form.save()
          
            application = Applications(
                type = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type")),
                applicant = request.user,details = form.cleaned_data.get("Approvals_type"),
                attachment = form.cleaned_data.get("attachments"),remarks = form.cleaned_data.get("remarks")
            )
            application.save()
            return JsonResponse("application submitted successfully",safe=False)


def Events(request):

    return render(request,'management/events.html')

def Post(request):

    return render(request,'management/post.html')

