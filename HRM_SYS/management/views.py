from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordResetView
from .forms import EmpForm,ApprovalForm,LeaveForm,Employee,UserRegForm,filesForm,profileForm,UserUpdateForm
from .models import *
from datetime import datetime,date
import time
# Create your views here.
@login_required
def home(request):
    todos = []
    for todo in Applications.objects.all():
        if request.user.username in todo.approvers.split(','):
            apps = [
                 todo.pk,todo.approvers,todo.created,todo.remarks
            ]
            todos.append(apps)
    context = {"todos":todos,"employees":Employee.objects.all()}
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
                emp_id = form.cleaned_data.get("username")
            )
       
            send_mail(
                subject='Beezy new login details',
                message='username: '+str(form.cleaned_data.get("username"))+'\n'+ "password: "+str(form.cleaned_data.get("password1"))+'\n'+"if you didn't register kindly ignore",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data.get("email")])
            employee.save()
            messages.success(request,f'{username} account created')
            return redirect('management-home')
    return render(request,'management/register.html',{'form':form})
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
@login_required
def upload_leave(request):
    if request.POST:
       form = LeaveForm(request.POST,request.FILES)
       if form.is_valid():
            form.instance.applicant = request.user
            form.save()
            approvers = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type"))
            approvers = [app.rstrip() for app in approvers.approvers.split('\n')]
           
            application = Applications(
                type = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type")),
                applicant = request.user,details = form.cleaned_data.get("remarks"),
                attachment = form.cleaned_data.get("attachments"),remarks = "",
                approvers = ",".join(approvers),expected = len(approvers)
                
            )
            application.save()
            return JsonResponse("application submitted successfully",safe=False)
@login_required    
def upload_process(request):
    if request.POST:
       form = ApprovalForm(request.POST,request.FILES)
       if form.is_valid():
            form.instance.applicant = request.user
            form.instance.created = datetime.now()
            form.save()
            approvers = Approvals.objects.get(name=form.cleaned_data.get("approvals"))
            approvers = [app.rstrip() for app in approvers.approvers.split('\n')]
          
            application = Applications(
                type = Approvals.objects.get(name=form.cleaned_data.get("approvals")),
                applicant = request.user,details = form.cleaned_data.get("details"),
                attachment = form.cleaned_data.get("attachments"),remarks = "",
                approvers = ",".join(approvers),expected = len(approvers),
               
                
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
            application.status = "completed"
        
        application.status = "pending"
        application.save()

        return JsonResponse("approved successfully",safe=False)


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



def Events(request):

    return render(request,'management/events.html')

def Post(request):

    return render(request,'management/post.html')

class EditEmpView(LoginRequiredMixin,UpdateView):
    
    model = Employee
    template_name = 'management/add_employees.html'
    fields = ['first_name','second_name','national_no','phone','address','location','account_no','bank_name']
    
    raise_exception = True
    success_url = '/list_employee'

    def form_valid(self,form):
        return super().form_valid(form)
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'management/password_reset.html'
    email_template_name = 'management/password_reset_email.html'
    subject_template_name = 'management/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    #success_url = reverse_lazy('users-home')    
