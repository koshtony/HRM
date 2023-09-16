from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Employee(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,default="None")
    second_name = models.CharField(max_length=50,default="None")
    email = models.EmailField(default="None")
    phone = models.CharField(max_length=50,default="None")
    next_kin_name = models.CharField(max_length=50,default="None")
    next_kin_id = models.CharField(max_length=50,default="None")




class Attendance(models.Model):

    employee = models.ForeignKey(Employee,on_delete=models.PROTECT)
    is_leave = models.BooleanField(default=False)


