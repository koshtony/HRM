from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from payroll.models import PayRollSetting
from tinymce.models import HTMLField
from datetime import date

import time
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    image = models.ImageField(default='user.jpeg',upload_to='profile_images')
    first = models.CharField(max_length=50,default="None")
    surname = models.CharField(max_length=50,default="None")
    email = models.EmailField(default="user@gmail.com")
    phone = models.CharField(max_length=20,default="None")
    activation = models.CharField(max_length=20,default="None")
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Department(models.Model):
    name = models.CharField(max_length=50,default="None")
    hod_username = models.CharField(max_length=50,default="None")
    size = models.FloatField(default=1)
    created = models.DateField(default=timezone.now)
    remarks = models.TextField(default="")
    
    def __str__(self):

        return self.name


class Roles(models.Model):
    name = models.CharField(max_length=50,default="None")
    requirements = models.CharField(max_length=50,default="None")
    created = models.DateField(default=timezone.now)
    remarks = models.TextField(default="")

    def __str__(self):

        return self.name

class Station(models.Model):

    name = models.CharField(max_length=100,null=True)
    created = models.DateField(default=timezone.now)

    def __str__(self):

        return self.name


class Employee(models.Model):
   
    emp_id = models.CharField(max_length=50,default="None")
   # personal details
    
    first_name = models.CharField(max_length=50,default="None")
    second_name = models.CharField(max_length=50,default="None")
    national_no = models.CharField(max_length=50,default="None")
    kra_pin = models.CharField(max_length=50,default="None")
    email = models.EmailField(default="None")
    dob = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=100,default="undisclosed",choices=(("male","male"),("female","female"),("undisclosed","undisclosed")))
    phone = models.CharField(max_length=50,default="None")
    next_kin_name = models.CharField(max_length=50,default="None")
    next_kin_id = models.CharField(max_length=50,default="None")
    next_kin_phone = models.CharField(max_length=50,default="None")
    address = models.CharField(max_length=50,default="None")
    location = models.CharField(max_length=50,default="None")
    station = models.ForeignKey(Station,on_delete = models.PROTECT,null=True)

 # HR admin section

    role = models.ForeignKey(Roles,on_delete = models.PROTECT,null=True)
    departments = models.ForeignKey(Department,on_delete = models.PROTECT,null=True)
    education_level = models.CharField(max_length=50,default="None")
    doj = models.DateField(default=timezone.now)
    dol = models.DateField(null=True)
    payroll_settings = models.ForeignKey(PayRollSetting,on_delete=models.PROTECT,null=True)
    
 # finance section 

    account_no = models.CharField(max_length=50,default="None")
    bank_name = models.CharField(max_length=50,default="None")
    salary = models.FloatField(default=0.0)
    allowance = models.FloatField(default=0.0)
    add_ons = models.FloatField(default=0.0)

# account management 
    other_fields = models.TextField(default="name:value")
    status = models.CharField(max_length=50,choices=(('incomplete',"incomplete"),('active',"active"),('resigned',"resigned"),('terminated',"terminated"),('suspended',"suspended")),default="None")
    image = models.ImageField(default='emoloyee.png',upload_to='emp_images')
    remarks = models.TextField(default="",null=True)





    def __str__(self):

        return self.emp_id
    
    def update(self,*args, **kwargs):
            for name,values in kwargs.items():
                try:
                    setattr(self,name,values)
                except KeyError:
                    pass
            self.save()
class AttSettings(models.Model):
    employee_id = models.CharField(max_length=100,null=True)
    start = models.TimeField(default=timezone.now())
    end = models.TimeField(default=timezone.now())
    deduction_per_day = models.FloatField(default=0.0)
    expected_days =  models.FloatField(default=24.0)
    leave_days =  models.FloatField(default=21.0)
    remarks = models.TextField(default="")
    address = models.CharField(max_length=300,default="")
    clock_in_latitude = models.CharField(max_length=1000,default="")
    clock_in_longitude = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.employee_id
class FilesCategory(models.Model):

    category_name = models.CharField(max_length=100)

    def __str__(self):

        return self.category_name
    
class EmpFiles(models.Model):

    employee = models.CharField(max_length=100)
    category = models.ForeignKey(FilesCategory,on_delete=models.PROTECT)
    file_name = models.CharField(max_length=100,default="none")
    document = models.FileField(default="document.pdf",upload_to='emp_files')
    properties = models.TextField(default="none")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.file_name





class Attendance(models.Model):

    employee = models.ForeignKey(Employee,on_delete=models.PROTECT)
    is_leave = models.BooleanField(default=False)
    day = models.DateField(default=timezone.now)
    clock_in = models.CharField(max_length=1000,default="")
    clock_out = models.CharField(max_length=1000,default="")
    lat = models.CharField(max_length=10,default="")
    long  = models.CharField(max_length=10,default="")
    lat1 = models.CharField(max_length=10,default="")
    long1 = models.CharField(max_length=10,default="")
    image1 =models.TextField()
    image2 =models.TextField()
    status = models.CharField(max_length=100,default="partial")
    counts = models.IntegerField(default=0)
    hours = models.FloatField(default=0.0)
    days = models.FloatField(default=0.0)
    leave_days = models.IntegerField(default=21)
    deductions = models.FloatField(default=0.0)
    created = models.DateTimeField(default=timezone.now)
    remarks = models.TextField()
   

    def __str__(self):

        return self.employee.emp_id
    



class Approvals(models.Model):

    name = models.CharField(max_length=100,default="")
    approvers = models.TextField(default="")
    created = models.DateField(default=timezone.now)
    remarks = models.TextField() 

    def __str__(self):
        return self.name

class Applications(models.Model):

    type = models.ForeignKey(Approvals,on_delete=models.PROTECT)
    applicant = models.ForeignKey(User,on_delete=models.PROTECT)
    approvers = models.TextField(default="")
    details = HTMLField()
    created_date = models.DateField(default=timezone.now)
    created_time = models.TimeField(default=timezone.now)
    attachment = models.FileField(default='attachment',upload_to='approval_files')
    status = models.CharField(max_length=10,choices=(('pending',"pending"),('cancelled',"cancelled"),('complete',"complete")),default="pending")
    stage = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    expected = models.IntegerField(default=0)
    start = models.DateField(default=timezone.now)
    end = models.DateField(default=timezone.now)
    days = models.IntegerField(default = 0)

    remarks = models.TextField()

    def __str__(self):
        return self.type.name
    
class approvalTrack(models.Model):

    application = models.ForeignKey(Applications,on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    comments = models.TextField(default="no comment")
    status = models.CharField(max_length=100,default="pending")
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    def __str__(self):

        return self.application.type.name

class Process(models.Model):

    applicant = models.ForeignKey(User,on_delete=models.PROTECT)
    approvals = models.ForeignKey(Approvals,on_delete=models.PROTECT,related_name="processes")
    details = HTMLField()
    created = models.DateField()
    attachments = models.FileField(default="process.pdf",upload_to='application_files')
    status = models.CharField(max_length=10,choices=(('pending',"pending"),('cancelled',"cancelled"),('complete',"complete")),default="pending")
   
    def __str__(self):

        return self.applicant.username

    
class Leave(models.Model):
    
    applicant = models.ForeignKey(User,on_delete=models.PROTECT,related_name="applicant")
    Approvals_type = models.ForeignKey(Approvals,on_delete=models.PROTECT,related_name="leave")
    category = models.CharField(max_length=100,choices=(("annual","annual"),("sick","sick"),("compassionate","compassionate"),("office","office")),default="")
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    days = models.FloatField(default=0)
    attachments = models.FileField(default="attachment.pdf",upload_to='application_files')
    status = models.CharField(max_length=30,default="pending")
    created = models.DateTimeField(default=timezone.now)
    details = models.TextField()

    def __str__(self):

        return self.category 
    



class Todo(models.Model):

    recpient_id = models.CharField(max_length=30,default="")
    details = models.TextField()
    links = models.CharField(max_length=200,default="")


    def __str__(self):

        return self.recpient_id
class Events(models.Model):

    title = models.CharField(max_length=100,default="")
    details = models.TextField()
    category = models.CharField(max_length=100,choices=(("announcement","announcement"),("events","events"),("updates","updates")),default="")
    viewers = models.CharField(max_length=100,choices=(("all","all"),("members","members"),("admins","admins")),default="")
    viewers_list = models.TextField(default="")
    created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    files = models.FileField(default='posts.png',upload_to='posts_files')

    def __str__(self):

        return self.title 
    
class Notifications(models.Model):

    recipient = models.ForeignKey(User,on_delete=models.PROTECT)
    info = models.TextField()
    url = models.CharField(max_length=100,default='')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    def __str__(self):

        return self.recipient.username
    

class ChatMessage(models.Model):
    
    body = HTMLField()
    anonymous = models.BooleanField(default=False)
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="msg_sender")
    anonymous_sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="anonymous_sender",null=True)
    recep = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="msg_recepient")
    sent = models.DateTimeField(default=timezone.now())
    seen = models.BooleanField(default=False)
    file = models.FileField(null=True,upload_to="chat_files")
    
    def __str__(self):
        
        return self.sender.user.username
    
