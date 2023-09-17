from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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
   
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=50,default="None")
   # personal details
    
    first_name = models.CharField(max_length=50,default="None")
    second_name = models.CharField(max_length=50,default="None")
    id_no = models.CharField(max_length=50,default="None")
    email = models.EmailField(default="None")
    phone = models.CharField(max_length=50,default="None")
    next_kin_name = models.CharField(max_length=50,default="None")
    next_kin_id = models.CharField(max_length=50,default="None")

 # HR admin section

    role = models.CharField(max_length=50,default="None")
    department = models.CharField(max_length=50,default="None")
    education_level = models.CharField(max_length=50,default="None")
    documents = models.FileField(default='documents.pdf',upload_to='documents')

 # finance section 

    account_no = models.CharField(max_length=50,default="None")
    bank_name = models.CharField(max_length=50,default="None")
    salary = models.FloatField(default=0.0)
    allowance = models.FloatField(default=0.0)
    add_ons = models.FloatField(default=0.0)
    finance_documents = models.FileField(default='documents.pdf',upload_to='bank_documents')

# account management 

    status = models.CharField(max_length=50,default="None")

    def __str__(self):

        return self.emp_id





class Attendance(models.Model):

    employee = models.ForeignKey(Employee,on_delete=models.PROTECT)
    is_leave = models.BooleanField(default=False)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    lat = models.CharField(max_length=10,default="")
    long  = models.CharField(max_length=10,default="")
    lat1 = models.CharField(max_length=10,default="")
    lat2 = models.CharField(max_length=10,default="")
    image1 =models.TextField()
    image2 =models.TextField()
    remarks = models.TextField()


