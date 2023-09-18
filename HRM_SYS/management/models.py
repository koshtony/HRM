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
    address = models.CharField(max_length=50,default="None")
    location = models.CharField(max_length=50,default="None")

 # HR admin section

    role = models.CharField(max_length=50,default="None")
    department = models.CharField(max_length=50,default="None")
    education_level = models.CharField(max_length=50,default="None")
    documents = models.FileField(default='documents.pdf',upload_to='documents')
    doj = models.DateField(default=timezone.now)
    dol = models.DateField(default=timezone.now)

 # finance section 

    account_no = models.CharField(max_length=50,default="None")
    bank_name = models.CharField(max_length=50,default="None")
    salary = models.FloatField(default=0.0)
    allowance = models.FloatField(default=0.0)
    add_ons = models.FloatField(default=0.0)
    finance_documents = models.FileField(default='documents.pdf',upload_to='bank_documents')

# account management 

    status = models.CharField(max_length=50,default="None")
    image = models.ImageField(default='emoloyee.png',upload_to='emp_images')

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


class Approvers(models.Model):

    Employee_ids = models.CharField(max_length=100,default="")
    approval_type = models.CharField(max_length=10,default="")
    created = models.DateField(default=timezone.now)
    remarks = models.TextField() 

class Approvals(models.Model):

    type = models.CharField(max_length=100,default="")
    approvers = models.ForeignKey(Approvers,on_delete=models.PROTECT)
    level = models.CharField(max_length=10,default="")
    created = models.DateField(default=timezone.now)
    remarks = models.TextField()

    def __str__(self):
        return self.type

class Process(models.Model):

    applicant = models.CharField(max_length=10,default="")
    approvals = models.ForeignKey(Approvals,on_delete=models.PROTECT,related_name="processes")
    details = models.TextField()
    created = models.DateField()
    status = models.CharField(max_length=10,choices=(('pending',"pending"),('cancelled',"cancelled"),('complete',"complete")),default="pending")
    documents = models.FileField(default="process.pdf",upload_to='process')

    
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



