from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordResetView
from .forms import EmpForm,ApprovalForm,LeaveForm,Employee,UserRegForm,filesForm,profileForm,UserUpdateForm
from .models import *
from payroll.models import PayRoll
from datetime import datetime,date
import folium
import time
import json
# Create your views here.
@login_required
def home(request):
    todos = []
    for todo in Applications.objects.all():
        if request.user.username in todo.approvers.split(','):
            apps = [
                 todo.pk,todo.approvers,todo.created_date,todo.details,todo.attachment.url
            ]
            todos.append(apps)
    event = Events.objects.last()
    department = Department.objects.all()
    payrolls = PayRoll.objects.filter(employee_id = request.user.username)
    context = {"todos":todos,"employees":Employee.objects.all(),"event":event,"department":department,"payrolls":payrolls}
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
        "applications":Applications.objects.all().order_by('-created_date'),
        "tracks":approvalTrack.objects.all()
        
        }

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
    
# create departments overview
def departments(request):

    departments = Department.objects.all()

    context =  {'departments':departments}

    return render(request,'management/departments.html',context)

def dep_details(request,name):

    details = Employee.objects.filter(departments = name)
    dep_attendance = Attendance.objects.filter(employee__departments = name)
    context = {"details":details,"attendances":dep_attendance}

    return render(request,'management/dep_details.html',context)


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

def get_employee(request):

    if request.POST:

        id = request.POST.get("id")

        print(id)

        employee = Employee.objects.get(emp_id = str(id))

        employee = serializers.serialize('json',[employee,])
        
        print(employee)
        return JsonResponse(employee, safe=False)



def list_files(request):

    context ={"files":EmpFiles.objects.all(),"file_form":filesForm()}
    if request.POST:
        file_form = filesForm(request.POST,request.FILES)
        if file_form.is_valid():
            file_form.save()
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

@login_required
def clock(request):

    context = {'leave_form':LeaveForm(),"approvals":Approvals.objects.all()}
   
    if request.POST:
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
            print(approvers)
            for approve in approvers:
                print(approve)
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
        print(application.approvers)

        application.stage +=1
        if application.stage == application.expected:
        
            application.status = "complete"
            application.rate = 100
            application.save()
            if application.type.name == "leave":
                
                att = Attendance(
                    employee = Employee.objects.get(emp_id = application.applicant.username),
                    is_leave = True,
                    days = application.days,
                    counts = application.days,
                    remarks = "leave "+str(application.start)+" to "+str(application.end),
                    image1 = "", 
                    image2 = ""
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
                
                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = ""
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

@login_required
def profile(request):

    profile_form = profileForm(instance=request.user.profile)
    user_form = UserUpdateForm(instance=request.user)

    context = {"profile_form":profile_form}

    if request.method=='POST':
    
        profile_forms = profileForm(request.POST,request.FILES,instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)
        if profile_forms.is_valid() and user_form.is_valid():
            user_form.save()
            profile_forms.save()
            

        return JsonResponse("profile updated",safe=False)


    return render(request,'management/profile.html',context)


''''
    displays both announcements and events
'''
def Event(request):

    events = Events.objects.all().order_by('-created')

    context = {
                "events":events,
    }

    return render(request,'management/events.html',context)

'''
    saves created post
'''
def add_event(request):

    if request.POST:
        
        title = request.POST.get("title"),
        category = request.POST.get("category")
        content = request.POST.get("content")
        print(content)

        events = Events(

              title = title , details = content , category =  category,
              created = datetime.now() , creator = request.user
        )
        events.save()

        

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
   folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
   folium.LayerControl().add_to(map)

  
   map = map._repr_html_()

   context = {
       'map':map
   }
   
   return render(request,'management/map.html',context)

def iframe_redirect(request):

    return render(request,'management/iframe_redirect.html')



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


