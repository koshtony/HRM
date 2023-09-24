from django.db import models
from management.models import *

# Create your models here.
class PayRoll(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT)
    total_hours = models.FloatField()
    expected_hours = models.FloatField()
    deductions = models.FloatField()
    leave_days = models.FloatField()
    gross_pay = models.FloatField()
    net_pay =  models.FloatField()

    def __str__(self):

        return self.employee.emp_id




class PayRollSettings(models.Model):

    total_tax = models.FloatField()
    nssf = models.FloatField()
    nhif = models.FloatField()
    others = models.FloatField()
    