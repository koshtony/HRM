from django.db import models
from django.utils import *
import datetime

# Create your models here.

class PayRoll(models.Model):
    payroll_id = models.CharField(max_length=100,null=True)
    employee_id = models.CharField(max_length=100,null=True)
    sign_id = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100,null=True)
    id_no = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=100,null=True)
    role = models.CharField(max_length=100,null=True)
    account_no = models.CharField(max_length=100,null=True)
    basic_salary = models.FloatField(default=0.0)
    allowance =  models.FloatField(default=0.0)
    add_ons = models.FloatField(default=0.0)
    total_hours = models.FloatField(default=0.0)
    leave_days = models.FloatField(default=0.0)
    deductions = models.FloatField(default=0.0) 
    gross_pay  = models.FloatField(default=0.0)
    taxable_income = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0) 
    nhif = models.FloatField(default=0.0)
    insurance = models.FloatField(default=0.0)
    housing = models.FloatField(default=0.0)
    others = models.FloatField(default=0.0)
    net_pay = models.FloatField(default=0.0)
    created = models.DateField(default=datetime.date.today())

    def __str__(self):

        return self.payroll_id

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

    