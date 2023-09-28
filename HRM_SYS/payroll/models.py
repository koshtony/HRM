from django.db import models
from django.utils import *
import datetime

# Create your models here.

class PayRoll(models.Model):
    payroll_id = models.CharField(max_length=1000,default=hash(datetime.datetime.now()))
    employee = models.ForeignKey("management.Employee",on_delete=models.PROTECT)
    total_hours = models.FloatField()
    expected_hours = models.FloatField()
    deductions = models.FloatField()
    leave_days = models.FloatField()
    gross_pay = models.FloatField()
    net_pay =  models.FloatField()

    def __str__(self):

        return self.employee.emp_id

tax_formula = '''24000=10%
8333=25%
467667=30%
300000=32.5%
'''
class PayRollSetting(models.Model):
    
    category = models.CharField(max_length=100)
    tax_rate = models.TextField(default=tax_formula)
    nssf = models.FloatField()
    nhif = models.FloatField()
    health_insurance = models.FloatField(default=0.0)
    housing = models.FloatField(default=0.0)
    others = models.FloatField()

    def __str__(self):

        return self.category

    