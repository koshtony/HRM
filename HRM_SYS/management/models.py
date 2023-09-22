from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
import time
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=50,default="None")
    hod = models.CharField(max_length=50,default="None")
    size = models.FloatField(default=1)
    created = models.DateField(default=timezone.now)
    remarks = models.TextField(default="")

class Roles(models.Model):
    name = models.CharField(max_length=50,default="None")
    requirements = models.CharField(max_length=50,default="None")
    created = models.DateField(default=timezone.now)
    remarks = models.TextField(default="")

class Employee(models.Model):
   
    emp_id = models.CharField(max_length=50,default="None")
   # personal details
    
    first_name = models.CharField(max_length=50,default="None")
    second_name = models.CharField(max_length=50,default="None")
    id_no = models.CharField(max_length=50,default="None")
    email = models.EmailField(default="None")
    dob = models.DateField(default=timezone.now)
    phone = models.CharField(max_length=50,default="None")
    next_kin_name = models.CharField(max_length=50,default="None")
    next_kin_id = models.CharField(max_length=50,default="None")
    next_kin_phone = models.CharField(max_length=50,default="None")
    address = models.CharField(max_length=50,default="None")
    location = models.CharField(max_length=50,default="None")

 # HR admin section

    role = models.CharField(max_length=50,default="None")
    department = models.CharField(max_length=50,default="None")
    education_level = models.CharField(max_length=50,default="None")
    doj = models.DateField(default=timezone.now)
    dol = models.DateField(default=timezone.now)

 # finance section 

    account_no = models.CharField(max_length=50,default="None")
    bank_name = models.CharField(max_length=50,default="None")
    salary = models.FloatField(default=0.0)
    allowance = models.FloatField(default=0.0)
    add_ons = models.FloatField(default=0.0)

# account management 

    status = models.CharField(max_length=50,default="None")
    image = models.ImageField(default='emoloyee.png',upload_to='emp_images')

    def __str__(self):

        return self.emp_id
class FilesCategory(models.Model):

    category_name = models.CharField(max_length=100)

    def __str__(self):

        return self.category_name
    
class EmpFiles(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    category = models.ForeignKey(FilesCategory,on_delete=models.PROTECT)
    file_name = models.CharField(max_length=100,default="none")
    document = models.FileField(default="document.pdf",upload_to='emp_files')
    properties = models.TextField(default="none")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.file_name





class Attendance(models.Model):

    employee = models.ForeignKey(User,on_delete=models.PROTECT)
    is_leave = models.BooleanField(default=False)
    day = models.DateField(default=date.today())
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
    remarks = models.TextField()
    

class AttSettings(models.Model):

    start = models.TimeField()
    end = models.TimeField()
    deduction_per_hour = models.FloatField()
    morning_deduction =  models.FloatField()
    evening_deduction = models.FloatField()
    expected_hours = models.FloatField()
    remarks = models.TextField()


class Approvals(models.Model):

    name = models.CharField(max_length=10,default="")
    approvers = models.ManyToManyField(Employee)
    created = models.DateField(default=timezone.now)
    remarks = models.TextField() 

    def __str__(self):
        return self.name

class Applications(models.Model):

    type = models.ForeignKey(Approvals,on_delete=models.PROTECT)
    applicant = models.ForeignKey(User,on_delete=models.PROTECT)
    details = models.TextField()
    created = models.DateField(default=timezone.now)
    attachment = models.FileField(default='attachment',upload_to='ápproval_files')
    remarks = models.TextField()

    def __str__(self):
        return self.type.name

class Process(models.Model):

    applicant = models.ForeignKey(User,on_delete=models.PROTECT)
    approvals = models.ForeignKey(Applications,on_delete=models.PROTECT,related_name="processes")
    details = models.TextField()
    created = models.DateField()
    status = models.CharField(max_length=10,choices=(('pending',"pending"),('cancelled',"cancelled"),('complete',"complete")),default="pending")
   
    def __str__(self):

        return self.applicant.username



    
class Leave(models.Model):
    
    applicant = models.ForeignKey(User,on_delete=models.PROTECT,related_name="applicant")
    Approvals_type = models.ForeignKey(Approvals,on_delete=models.PROTECT,related_name="leave")
    category = models.CharField(max_length=100,choices=(("annual","annual"),("sick","sick"),("compassionate","compassionate"),("office","office")),default="")
    start = models.DateTimeField()
    end = models.DateTimeField()
    attachments = models.FileField(default="attachment.pdf",upload_to='leave')
    status = models.CharField(max_length=30,default="pending")
    created = models.DateTimeField(default=timezone.now)
    remarks = models.TextField()

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
    category = models.CharField(max_length=100,choices=(("announcement","announcement"),("events","events")),default="")
    created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):

        return self.title

class Posts(models.Model):
    
    post = models.TextField()
    created = models.DateTimeField()
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):

        return str(self.pk)