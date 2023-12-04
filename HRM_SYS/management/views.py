from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import *
from django.http import JsonResponse,HttpResponse,FileResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Count,Sum
from django.db.models.functions import ExtractMonth
from .forms import EmpForm,ApprovalForm,LeaveForm,Employee,UserRegForm,filesForm,profileUpdateForm,UserUpdateForm,ChatForm,PostsForm,SettingsForm,CreateApprovalForm
from .models import *
from .temps import gen_temp
from payroll.models import PayRoll
from datetime import datetime,date,timedelta
import string
import pandas
import numpy 
import math
import folium
import time
import json
import os
# Create your views here.
@login_required

def home(request):
    todos = []
    for todo in Applications.objects.all():
        if request.user.username == todo.approvers.split(',')[0]:
            apps = [
                 todo.pk,todo.approvers,todo.created_date,todo.details,todo.attachment.url,todo.type.name,f'{Employee.objects.filter(emp_id = todo.applicant.username)[0].first_name}' if len(Employee.objects.filter(emp_id = todo.applicant.username))>0 else f'{todo.applicant.username} name not found'
            ]
            todos.append(apps)
    print(todos)
    event = Events.objects.last()
    department = Department.objects.all()
    payrolls = PayRoll.objects.filter(employee_id = request.user.username).order_by('-created_date')[:4]
    attendance = Attendance.objects.filter(employee__emp_id = request.user.username).order_by('-day')[:5]
    context = {"todos":todos,"employees":Employee.objects.all(),"event":event,"department":department,"payrolls":payrolls,"attendance":attendance}
    return render(request,'management/index.html',context)
@login_required
def register(request):
    form=UserRegForm()
    if request.method=='POST':
        form=UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")


            employee = Employee(
                emp_id = form.cleaned_data.get("username"),
                status = 'incomplete'
            )
       
            send_mail(
                subject='Beezy new login details',
                message='username: '+str(form.cleaned_data.get("username"))+'\n'+ "password: "+str(form.cleaned_data.get("password1"))+'\n'+"if you didn't register kindly ignore",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data.get("email")])
            

            employee.save()

            new_profile = Profile(user=User.objects.get(username = username))
            new_profile.save()

            messages.success(request,f'{username} account created')
            
            return redirect('management-home')
    return render(request,'management/register.html',{'form':form})
def add_info(request):

    return render(request,'management/add_info.html')

def approvals(request):
    context = {"appForm":ApprovalForm}
    return render(request,'management/approvals.html',context)

def view_approvals(request):

    context = {
        "applications":Applications.objects.all().filter(applicant=request.user).order_by('-pk'),
        "tracks":approvalTrack.objects.all()
        
        }

    return render(request,'management/approval_list.html',context)

@csrf_exempt
def get_approvals_name(request):

    if request.POST:
        pk = request.POST.get("pk")
      
        apps = Applications.objects.get(pk=pk)
        names = []
        for id in apps.type.approvers.split('/n'):

            if id in apps.approvers.split(','):
            
                try:
                    Employee.objects.get(emp_id = id)

                    names.append({"name":str(Employee.objects.get(emp_id = id).first_name)+" "+str(Employee.objects.get(emp_id = id).second_name),"status":"approved"})
                except:

                    names.append({"name":"couldn't find name for "+str(id),"status":"approved"})
            else:

                try:
                    Employee.objects.get(emp_id = id)

                    names.append({"name":str(Employee.objects.get(emp_id = id).first_name)+" "+str(Employee.objects.get(emp_id = id).second_name),"status":"pending"})
                except:

                    names.append({"name":"couldn't find name for "+str(id),"status":"pending"})


        return JsonResponse(names,safe=False)





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
    
# create departments overview

def departments(request):

    departments = Department.objects.all()

    context =  {'departments':departments}

    return render(request,'management/departments.html',context)

def dep_details(request,name):

    details = Employee.objects.filter(departments=Department.objects.get(name=name))
    dep_attendance = Attendance.objects.filter(employee__departments = Department.objects.get(name=name))
    context = {"details":details,"attendances":dep_attendance}

    return render(request,'management/dep_details.html',context)


def add_department(request):

    pass

def add_roles(request):

    pass

def add_employee(request):

    context = {"emp_form":EmpForm()}

    return render(request,'management/add_employees.html',context)
@csrf_exempt
def resign_employee(request):

    if request.POST:

        emp_id = request.POST.get("emp_id")
        remarks = request.POST.get("remarks")

        emp = Employee.objects.get(emp_id=emp_id)
        emp.status = "resigned"
        emp.remarks = remarks
        emp.dol = datetime.now()
        emp.save()

        user_del = User.objects.get(username = emp_id)
        user_del.delete()

        return JsonResponse("resignation successfully set",safe=False)



def list_employee(request):
    
    dep_count =  Employee.objects.values('departments__name').annotate(all_deps = Count('departments__name'))

    turnovers = Employee.objects.values('status').annotate(all_status = Count('status'))

    joining_trends = Employee.objects.annotate(month=ExtractMonth('doj')).values('month').annotate(size=Count('month'))

    resign_trends = Employee.objects.annotate(month=ExtractMonth('dol')).values('month').annotate(size=Count('month'))

    try:

        rate = (len([turnover["status"] for turnover in turnovers if turnover["status"] == "resigned" ])/((len([turnover["status"] for turnover in turnovers if turnover["status"] == "resigned" ])+len([turnover["status"] for turnover in turnovers if turnover["status"] == "active" ]))/2))*100
    except:
        rate = 0;
    
    print(resign_trends)
    context = {
        
        "employee":Employee.objects.all(),

        "dep_names":[dep["departments__name"] for dep in dep_count],

        "dep_total":[dep["all_deps"] for dep in dep_count],

        "status": [turnover["status"] for turnover in turnovers],

        "total_status":[turnover["all_status"] for turnover in turnovers],

        "rate": rate,

        "month":[trend["month"] for trend in joining_trends],

        "size":[trend["size"] for trend in joining_trends],

        "r_month":[trend["month"] for trend in resign_trends],

        "r_size":[trend["size"] for trend in resign_trends]

        }
    
    return render(request,'management/list_employees.html',context)

def get_employee(request):

    if request.POST:

        id = request.POST.get("id")

      

        employee = Employee.objects.get(emp_id = str(id))

        employee = serializers.serialize('json',[employee,])
        
        print(employee)
        return JsonResponse(employee, safe=False)
    
def employee_profile(request,id):

    employee = Employee.objects.get(emp_id = id)

    context = {"employee":employee}

    return render(request,'management/employee_profile.html',context)

@csrf_exempt   
def get_emp_other_details(request):

    if request.POST:

        emp_id = request.POST.get("id")

        other_fields = Employee.objects.get(emp_id = emp_id ).other_fields.split("\n")
        
        other_fields_all = []
        for other_field in other_fields:
            
            other_fields_all.append({"name":str(other_field.split(":")[0]),"value":str(other_field.split(":")[1])})
        
        return JsonResponse(other_fields_all,safe=False)

def get_employee_template(request):

    filename = 'employee_template.xlsx'

    filepath =  os.path.join(settings.MEDIA_ROOT, 'emp_temp',filename)
    gen_temp(filepath)

    path = open(filepath,'rb')

    response = FileResponse(path,as_attachment=True)

    return response
@csrf_exempt
def import_employee_data(request):

        try:
            file = request.FILES.get("file")
            emp_df = pandas.read_excel(file ,sheet_name='employee')
            settings_df = pandas.read_excel(file,sheet_name='attendance')
            settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()] = settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()].applymap(lambda x:math.trunc(x) if math.isnan(x)==False else 0)
            for items in emp_df.to_dict('records'):
                # create the user

                passwd = str(hash(date.today()))+str(items["emp_id"])
                # load employe data
                if Employee.objects.filter(emp_id=items["emp_id"]).exists() == False:
                    emp = Employee(
                        emp_id = items["emp_id"], first_name = items["first_name"],second_name = items["second_name"],national_no = items["national_no"],
                        kra_pin = items["kra_pin"],email = items["email"],dob=items["dob"],phone=items["phone"],next_kin_name = items["next_kin_name"],next_kin_id=items["next_kin_id"],
                        next_kin_phone = items["next_kin_phone"],address = items["address"],location = items["location"],station = Station.objects.filter(name = items["station_id"])[0],
                        role = Roles.objects.filter(name = items["role_id"])[0],departments = Department.objects.filter(name = items["departments_id"])[0], education_level = items["education_level"],doj=items["doj"],
                        dol = items["dol"],payroll_settings = PayRollSetting.objects.filter(category = items["payroll_settings_id"])[0],
                        account_no = items["account_no"], bank_name = items["bank_name"],salary = items["salary"],
                        allowance = items["allowance"], add_ons = items["add_ons"],status = "incomplete"

                    )
                    emp.save()
                else:

                    return JsonResponse(str(items["emp_id"])+" already exists",safe=False)
                # create user
                user = User(
                    username = math.trunc(items["emp_id"]),password=passwd,email = items["email"]
                )
                user.save()

                # create the profile
                profile = Profile(user=User.objects.get(username = items["emp_id"]))
                profile.save()

                

                send_mail(
                    subject='Beezy new login details',
                    message='username: '+str(items["emp_id"])+'\n'+ "password: "+str(passwd)+'\n'+"if you didn't register kindly ignore",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[items['email']])


            for items in settings_df.to_dict('records'):
                sett = AttSettings(
                    **items
                )
                sett.save()

            return JsonResponse("done",safe=False)
        
        except Exception as err:

            return JsonResponse(str(err),safe=False)


@csrf_exempt
def import_att_settings(request):

    try:

        file = request.FILES.get("file")
        settings_df = pandas.read_excel(file,sheet_name='attendance')
        for items in settings_df.to_dict('records'):
            sett = AttSettings(
                    **items
                )
            sett.save()
            return JsonResponse("done",safe=False)
    except Exception as err:

        return JsonResponse(str(err),safe=False)



@csrf_exempt
def lookup_employee(request):

    try:

        file = request.FILES.get("file")
        settings_df = pandas.read_excel(file,sheet_name='employee')
        settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()] = settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()].applymap(lambda x:math.trunc(x) if math.isnan(x)==False else 0)
        for items in settings_df.to_dict('records'):
            employee = Employee.objects.get(emp_id = items["emp_id"])
            print(employee)
            employee.update(**items)
            
        return JsonResponse("done",safe=False)
    except Exception as err:

        return JsonResponse(str(err),safe=False)




    


def list_files(request):

    context ={"files":EmpFiles.objects.all(),"file_form":filesForm()}
    if request.POST:
        file_form = filesForm(request.POST,request.FILES)

        if file_form.is_valid():
            instance = file_form.save(commit = False)
            instance.properties = file_form.cleaned_data.get("document")
            instance.save()
            
            return JsonResponse("file uploaded successfully",safe=False)
    return render(request,'management/files.html',context)

def get_emp_files(request):

    if request.POST:
        emp_id = request.POST.get("emp_id")
        emp_id = str(emp_id)
        my_files = EmpFiles.objects.filter(employee=Employee.objects.get(emp_id="001"))
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
    
def files_details(request,id):

        emp_files = EmpFiles.objects.filter(employee=Employee.objects.get(emp_id=id))
        app_files = Applications.objects.filter(applicant = User.objects.get(username = id ))
        
        context = {
            "emp_files":emp_files,
            "app_files":app_files
        }

        return render(request,'management/files_details.html',context)
# delete all selected files
@csrf_exempt
def files_del(request):

    if request.POST:

        pks = request.POST.get("pks")
        count = 0
        for pk in pks.split(","):
            # get file primary key and delete
            EmpFiles.objects.get(pk=pk).delete()
            count+=1
        
        return JsonResponse(str(count)+" file(s) deleted successfully",safe=False)

@login_required
def clock(request):

    context = {'leave_form':LeaveForm(),"approvals":Approvals.objects.all()}
   
    if request.POST:

        try:

            if len(AttSettings.objects.filter(employee_id = request.user.username))< 1:

                return JsonResponse("no settings found, contact admin",safe=False)

            att_settings =  AttSettings.objects.filter(employee_id = request.user.username)[0]
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
                        deductions  = 0,
                        days = 1

                        

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
                att_filt[0].deductions =  0
                att_filt[0].save()

                return JsonResponse("clock out successful",safe=False)
            
            elif att_filt[0].clock_in != '' and att_filt[0].clock_out != '':

                return JsonResponse("clock in and clockout already completed",safe=False)
            elif (datetime.now().hour > 14 and datetime.now().hour <= 24) and len(att_filt):

                attendance = Attendance(
                        employee =  Employee.objects.get(emp_id = request.user.username),
                        day = date.today(),
                        clock_in = empty,
                        clock_out = datetime.now(),
                        lat = empty ,long=empty,image1=empty,
                        lat1 = lat, long1 = long, image2 = image_info,remarks="clock out",
                        deductions  = 0,
                        days = 1

                        

                    )
                attendance.save()
                return JsonResponse("clock in successful",safe=False)


        except Exception as e:


            return JsonResponse(str(e),safe=False)


            



    return render(request,'management/clock.html',context)

def get_attendance(request):

    today_att = Attendance.objects.filter(day=date.today()).filter(employee = Employee.objects.get(emp_id=request.user.username))
    att_settings = AttSettings.objects.filter(employee_id = request.user.username)

    if len(att_settings)>0:

        att_settings = att_settings[0]

        if len(today_att) > 0:

            details = {
                "clock_in":today_att[0].clock_in,
                "clock_out":today_att[0].clock_out,
                "h1":att_settings.start.hour,
                "m1":att_settings.start.minute,
                "h2":att_settings.end.hour,
                "m2":att_settings.end.minute,
                "lat1":att_settings.clock_in_latitude,
                "long1":att_settings.clock_in_longitude
            }

            return JsonResponse(details,safe=False)
        
        details = {"h1":att_settings.start.hour,
                "m1":att_settings.start.minute,
                "h2":att_settings.end.hour,
                "m2":att_settings.end.minute,
                "clock_in":"",
                "clock_out":"",
                "lat1":att_settings.clock_in_latitude,
                "long1":att_settings.clock_in_longitude
            }
        print(details)
        return JsonResponse(details,safe=False)
    else:

        details = {
            "error":"no settings found"

            }
        
        return JsonResponse(details,safe=False)

def view_attendance(request):

    attendances =  Attendance.objects.all().order_by('-pk')
    leaves = Attendance.objects.filter(is_leave = True).order_by('-pk')
    #print(attendances)
    today_leaves = []
    for leave in leaves:
        print([datetime.strptime(leave.remarks.split(' ')[1],'%Y-%m-%d').date() + timedelta(days=i) for i in range((datetime.strptime(leave.remarks.split(' ')[3],'%Y-%m-%d').date() - datetime.strptime(leave.remarks.split(' ')[1],'%Y-%m-%d').date()).days + 1)])
        if date.today() in [datetime.strptime(leave.remarks.split(' ')[1],'%Y-%m-%d').date() + timedelta(days=i) for i in range((datetime.strptime(leave.remarks.split(' ')[3],'%Y-%m-%d').date() - datetime.strptime(leave.remarks.split(' ')[1],'%Y-%m-%d').date()).days + 1)]:

            today_leaves_dict = {
                "employee_id":leave.employee.emp_id,
                "name":leave.employee.first_name+ " "+leave.employee.second_name ,
                "day":leave.day,
                "days":leave.days,
                "leave_days":leave.leave_days,
                "created":leave.created,
                "status":leave.status,
                "remarks":leave.remarks
            }
            today_leaves.append(today_leaves_dict)


    late = []
    for attendance in attendances:
         if attendance.clock_in != '':
            try:
                if datetime.strptime(attendance.clock_in, '%Y-%m-%d %H:%M:%S.%f').time() > AttSettings.objects.get(employee_id = attendance.employee.emp_id).start:
             
                    late_dict = {
                    "employee":attendance.employee.emp_id,
                    "employee_name":attendance.employee.first_name + " "+attendance.employee.second_name,
                    "day":attendance.day,
                    "clock_in":attendance.clock_in,
                    "clock_out":attendance.clock_out,
                    "set_clock_in":AttSettings.objects.get(employee_id = attendance.employee.emp_id).start,
                    "set_clock_out":AttSettings.objects.get(employee_id = attendance.employee.emp_id).end,
                    "count": attendance.days,
                    "status":attendance.status,
                    

                }
                    late.append(late_dict)
            except:
                late_dict = {}
    absents = []

    for employee in Employee.objects.all():
        if employee.emp_id not in [att.employee.emp_id for att in Attendance.objects.filter(day = date.today())]:
            
            try:
                absent_dict = {
                    "employee_id":employee.emp_id,
                    "name":employee.first_name + employee.second_name ,
                    "email":employee.email ,
                    "phone":employee.phone ,
                    "next_of_kin":employee.next_kin_name,
                    "next_kin_phone":employee.next_kin_phone,
                    "address":employee.address + employee.location,
                    "set_clock_in":AttSettings.objects.get(employee_id = employee.emp_id).start,
                    "expected_days":AttSettings.objects.get(employee_id = employee.emp_id).expected_days
                }
            except:
                absent_dict = {
                    "employee_id":employee.emp_id,
                    "name":employee.first_name + employee.second_name ,
                    "email":employee.email ,
                    "phone":employee.phone ,
                    "next_of_kin":employee.next_kin_name,
                    "next_kin_phone":employee.next_kin_phone,
                    "address":employee.address + employee.location,
                    "set_clock_in":"no settings",
                    "expected_days":"no settings"
                }


            absents.append(absent_dict)

    context = {"attendances":attendances,"lates":late, "leaves":today_leaves,"absents":absents}

    return render(request,'management/list_attendance.html',context)

def edit_att_settings(request,emp_id):

    settings = AttSettings.objects.filter(employee_id = emp_id)[0]

    context = {"settings":settings,"form":SettingsForm()}

    if request.POST:
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request,'management/edit_attendance.html',context)
@csrf_exempt
def create_approval(request):
    
    if request.POST:

        approval = request.POST.get("approval")
        approvers = "\n".join(request.POST.get("approvers").split(','))

        apps = Approvals(

            name = approval, 
            approvers = approvers,
            created = datetime.now(),
            remarks = "created by -> "+str(request.user.username)
        )
        apps.save()

        return JsonResponse("created successfully",safe=False)


    context = {"employees":Employee.objects.all(),"form":CreateApprovalForm()}
    return render(request,'management/create_approval.html',context)
@csrf_exempt
def get_approval_temp(request):

    if request.POST:
        approval = request.POST.get("approval")
       
        try:

            data = Applications.objects.filter(type=Approvals.objects.get(pk=int(approval))).filter(applicant=request.user).filter(status="complete")[0].details
            print(data)
            return JsonResponse(data,safe=False)
        except:

            data = Approvals.objects.filter(pk=int(approval))[0].template
         
            return JsonResponse(data,safe=False)

        

@login_required
def upload_leave(request):
    if request.POST:
       form = LeaveForm(request.POST)
       if form.is_valid():
            
            form.instance.applicant = request.user
            form.save()
            
            approvers = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type"))
            approvers = [app.rstrip() for app in approvers.approvers.split('\n') if app!=request.user.username]
           
            application = Applications(
                type = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type")),
                applicant = request.user,details = form.cleaned_data.get("details"),
                attachment = form.cleaned_data.get("attachments"),remarks = "",
                approvers = ",".join(approvers),expected = len(approvers),
                created_date = datetime.now(),created_time = datetime.now(),
                start = form.cleaned_data.get("start"), end = form.cleaned_data.get("end"),
                days = form.cleaned_data.get("days")

    
            )

            application.save()


            return JsonResponse("application submitted successfully",safe=False)
@login_required    
def upload_process(request):
    if request.POST:
       form = ApprovalForm(request.POST,request.FILES)
       if form.is_valid():
            ''''
            form.instance.applicant = request.user
            form.instance.created = datetime.now()
            form.save()
            '''
            approvers = Approvals.objects.get(name=form.cleaned_data.get("approvals"))
            approvers = [app.rstrip() for app in approvers.approvers.split('\n') if app!=request.user.username]
     
            for approve in approvers:
            
                notify = Notifications(
                    recipient = User.objects.get(username=approve),
                    info = str(request.user.username)+" "+str(form.cleaned_data.get("approvals"))+" new approval",
                    date = datetime.now(),
                    time = datetime.now(),
                    url = "{}"
         
                )

                notify.save()
          
            application = Applications(
                type = Approvals.objects.get(name=form.cleaned_data.get("approvals")),
                applicant = request.user,details = form.cleaned_data.get("details"),
                attachment = form.cleaned_data.get("attachments"),remarks = "",
                approvers = ",".join(approvers),expected = len(approvers),
                created_date = datetime.now(),
                created_time = datetime.now()
               
                
            )
            application.save()

            
            return JsonResponse("application submitted successfully",safe=False)
    


'''
processing all approvals
'''
@login_required
def approve(request):

    if request.POST:
        id = request.POST.get("id")
        application = Applications.objects.get(pk=id)
        application.approvers = ",".join([i for i in application.approvers.split(',') if i!=request.user.username])
        #print(application.approvers)

        application.stage +=1
        if application.stage == application.expected:
        
            application.status = "complete"
            application.rate = 100
            application.save()
            if application.type.name == "leave":
                
                    leave_days = AttSettings.objects.get(employee_id = application.applicant.username ).leave_days

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        leave_days = leave_days - application.days
                        
                    )

                    att.save()
        else:
            application.status = "pending"
            application.rate = int((application.stage / application.expected)*100)
            application.save()



        return JsonResponse("approved successfully",safe=False)

@login_required
def reject_approval(request):

    if request.POST:

        id = request.POST.get("id")
        application = Applications.objects.get(pk=id)
        application.status = "rejected"
        application.approvers = ''
        application.save()

        return JsonResponse("rejected successfully",safe=False)
@login_required() 
def approve_by_details(request):

    if request.POST:
        id = request.POST.get("id")
        status = request.POST.get("status")
        comments = request.POST.get("comments")

        if status == "approve":
            application = Applications.objects.get(pk=id)
            application.approvers = ",".join([i for i in application.approvers.split(',') if i!=request.user.username])
            print(application.approvers)

            application.stage +=1
            if application.stage == application.expected:
                application.status = "complete"
                application.rate = 100
                application.save()
                if application.type.name == "leave":
                    
                    leave_days = AttSettings.objects.get(employee_id = application.applicant.username ).leave_days
                    

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        leave_days = leave_days - application.days
                        
                    )

                    att.save()

                track = approvalTrack(
                application = Applications.objects.get(pk=id),
                user = request.user,
                comments = comments,
                status = status,
                date = date.today(),
                time = datetime.now()
                )
            else:
                application.status = "pending"
                application.rate = int((application.stage // application.expected)*100)
                application.save()
             
                track = approvalTrack(
                    application = Applications.objects.get(pk=id),
                    user = request.user,
                    comments = comments,
                    status = status,
                    date = date.today(),
                    time = datetime.now()
                )
                track.save()
        
            return JsonResponse("approved successfully",safe=False)
        elif status == "reject":
            application = Applications.objects.get(pk=id)
            application.status = "rejected"
            application.approvers = ''
            application.save()

            track = approvalTrack(
                application = Applications.objects.get(pk=id),
                user = request.user,
                comments = comments,
                status = status,
                date = date.today(),
                time = datetime.now()
            )
            track.save()

            return JsonResponse("application rejected successfully",safe=False)
        
def recall_approval(request):

    if request.POST:

        pk = request.POST.get("id")

        if Applications.objects.get(pk=pk).stage > 0:

            return JsonResponse("application already read cannot be recalled, add comment instead",safe=False)
        else:

            application = Applications.objects.get(pk=pk)
            application.status = "cancelled"
            application.save()

            return JsonResponse("recalled successful",safe=False)

def recall_by_comment(request):

    if request.POST:

        remark = request.POST.get("remark")
        id = request.POST.get("id")
        print(id)
        application = Applications.objects.get(pk = id)
        track = approvalTrack(
            application = application,
            user = request.user,
            comments =remark,
            status = "cancelled",
            date = datetime.now(),
            time = datetime.now()
        )
        track.save()
        return JsonResponse("remark added successfully",safe=False)
@csrf_exempt
def view_approval_details(request):

    if request.POST:

        id = request.POST.get("id")

        details = Applications.objects.get(pk=id).details
        

        return JsonResponse(details,safe=False)
@login_required
def profile(request):
    try:
        profile_form = profileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)


        context = {"profile_form":profile_form,"password_form":password_form, "profiles":Profile.objects.all()}

        if request.method == 'POST':

        
            profile_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
            
            
            if profile_form.is_valid():
        
                profile_form.save()
                

            return JsonResponse("profile updated",safe=False)
    except Exception as error:

        context = {}

        
        


    return render(request,'management/profile.html',context)

# changing current user passwords
@login_required
def change_password(request):

    if request.POST:
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():

            new_user = form.save()
            update_session_auth_hash(request, new_user) 
            
            return JsonResponse("password updated successfully",safe=False)
        else:
            return JsonResponse("check the errors and correct",safe=False)

''''
    displays both announcements and events
'''
def Event(request):
    
    events = Events.objects.all().order_by('-created')
    all_events = []
    for event in events:

        event_dict = {

            "title":event.title,
            "details":event.details,
            "created":event.created,
            "image":event.creator.profile.image.url,
            "file":event.files.url,
            "viewers_list":event.viewers_list.split(','),
            "viewers":event.viewers
        }
        all_events.append(event_dict)
    
    context = {"events":all_events,"form":PostsForm()}

    return render(request,'management/events.html',context)

'''
    saves created post
'''
def add_event(request):

    if request.method == 'POST':
        
       post_form = PostsForm(request.POST,request.FILES)

       if post_form.is_valid():
           
           instance = post_form.save(commit=False)
           instance.creator = request.user
           if instance.viewers == "all":
               instance.viewers_list = ",".join([user.username for user in User.objects.all()])
           elif instance.viewers == "admins":
               instance.viewers_list = ",".join([user.username for user in User.objects.all() if user.is_staff])
           elif instance.viewers == "members":
               department = Employee.objects.get(emp_id=request.user.username).departments
             
               instance.viewers_list = ",".join([emp.emp_id for emp in Employee.objects.filter(departments=department)])

           instance.save()

           #print("yes")

           return JsonResponse("created successfully",safe=False)


def del_event(request):

    if request.POST:

        pk = request.POST.get("pk")

        Events.objects.get(pk=pk).delete()

        return JsonResponse("deleted successfully",safe=False)

def Post(request):

    return render(request,'management/post.html')

def get_notify(request):

    notifications = Notifications.objects.filter(recipient=request.user)
    popups = []
    for notification in notifications:
        notifs = {
            "image":notification.recipient.profile.image.url,"info":notification.info,
            "date":notification.date,"time":notification.time
            
            }
        popups.append(notifs)
        
    
    notifications = json.dumps(popups,default=str)


    return JsonResponse(notifications,safe=False)

def show_map(request,coords):
   
   coords = [float(cord) for cord in coords.split('_')]
   print(coords)
   map = folium.Map(coords)
   folium.Marker(coords).add_to(map)
   folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
   folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
   folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)in javascript
   folium.LayerControl().add_to(map)

  
   map = map._repr_html_()

   context = {
       'map':map
   }
   
   return render(request,'management/map.html',context)

def iframe_redirect(request):

    return render(request,'management/iframe_redirect.html')


def live_chat(request):

    profiles = Profile.objects.all()
    contxt = {
        
        "profiles":profiles
    }
    return render(request,'management/chats.html',contxt)


def live_chat_user(request,pk):
    
    
    ind_profile = Profile.objects.get(user_id=pk)
    profiles = Profile.objects.all()
    chats = ChatMessage.objects.all()
    in_chats = ChatMessage.objects.filter(sender = ind_profile , recep = request.user.profile)
    in_chats.update(seen=True)
    chat_form = ChatForm()

    contxt = {
        "profiles":profiles,
        "ind":ind_profile,
        "chats":chats,
        "counts":in_chats.count(),
        "form": chat_form
    }
    if request.method=="POST":
        c_form = ChatForm(request.POST)
        if c_form.is_valid():
            chat_msg = c_form.save(commit=False)
            chat_msg.sender = request.user.profile 
            chat_msg.recep = ind_profile 
            chat_msg.save()
            
            
    
    return render(request,'management/chat.html',contxt)
@csrf_exempt
def sent_msg(request,pk):
    
        ind_profile = Profile.objects.get(user_id=pk)
        
        data = json.loads(request.body)
        
        # filter chat from the req body
        chat = data["msg"]
        anony = data["anony"]
      
   
        #Profile.objects.get(user__username="hummingbird")
        if anony == "yes":
     
            new_chat = ChatMessage(
                body = chat , 
                sender = Profile.objects.get(user__username="anonymous") ,
                anonymous_sender = request.user.profile,
                recep = ind_profile,
                sent = datetime.now(),
                seen = False
                
                )
            new_chat.save()
            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)
       
        else:
           
            new_chat = ChatMessage(
                body = chat , 
                sender = request.user.profile,
                anonymous_sender = request.user.profile,
                recep = ind_profile,
                sent = datetime.now(),
                seen = False
                
                )
            new_chat.save()
            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)

            
@csrf_exempt
def chat_reply(request):

 

        data = json.loads(request.body)

        id = data["id"]
        msg = data["msg"]
        anony = data["anony"]

        chats = ChatMessage.objects.get(pk=id)

        if anony!="yes":
            new_chat = ChatMessage(
                body = msg , 
                sender = request.user.profile,
                anonymous_sender = request.user.profile,
                recep = chats.sender,
                sent = datetime.now(),
                seen = False
                
                )
            new_chat.save()
            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)
        else:

            new_chat = ChatMessage(
                body = msg, 
                sender = Profile.objects.get(user__username="anonymous") ,
                anonymous_sender = request.user.profile,
                recep = chats.anonymous_sender,
                sent = datetime.now(),
                seen = False
                
                )
            new_chat.save()

            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)





def chat_notify(request):
    
    
    usrs = Profile.objects.all()

    
    
    usrs_arr,chats_arr,send_arr,dates_arr = [],[],[],[]

    for usr in usrs:
        chats = ChatMessage.objects.filter(sender__id = usr.id , recep = request.user.profile,seen=False)
        usrs_arr.append(chats.count())
        for chat in chats:
            chats_arr.append(chat.body)
            send_arr.append(chat.sender.user.username)
            dates_arr.append(chat.sent)

    res_dict = {

                    "no":usrs_arr,"msg":chats_arr,"sender":send_arr,"dates":dates_arr,

                    


                }
    return JsonResponse(res_dict,safe=False)


def recv_msg(request,pk):
    
    ind_profile = Profile.objects.get(user_id=pk)
    
    chats = ChatMessage.objects.filter(sender = ind_profile , recep = request.user.profile)
    
    chats_arr = []
    
    for chat in chats:
        
        chats_arr.append(chat.body)
        
    return JsonResponse(chats_arr,safe=False)

def del_chat(request):

    if request.POST:

        id = request.POST.get("id")

        mssg_del = ChatMessage.objects.get(pk=id)

        mssg_del.delete()

        return JsonResponse("message deleted",safe=False)

class EditEmpView(LoginRequiredMixin,UpdateView):
    
    model = Employee
    template_name = 'management/add_employees.html'
    fields = '__all__'
    
    raise_exception = True

    success_url = '/iframe_redirect'
   

    def form_valid(self,form):
        return super().form_valid(form)
    
    

    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'management/password_reset.html'
    email_template_name = 'management/password_reset_email.html'
    subject_template_name = 'management/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('management-home')    


'''
    ===============data Analytics views===================

'''