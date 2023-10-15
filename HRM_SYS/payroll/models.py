from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class PayRoll(models.Model):
    org_name = models.CharField(max_length=100,null=True)
    payroll_id = models.CharField(max_length=100,null=True)
    employee_id = models.CharField(max_length=100,null=True)
    sign_id = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100,null=True)
    id_no = models.CharField(max_length=100,null=True)
    pin_no = models.CharField(max_length=100,null=True)
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
    nssf = models.FloatField(default=0.0)
    insurance = models.FloatField(default=0.0)
    housing = models.FloatField(default=0.0)
    others = models.FloatField(default=0.0)
    net_pay = models.FloatField(default=0.0)
    created = models.DateField(default=timezone.now)
    status = models.CharField(max_length=100,default="audit")
    pay_run = models.CharField(max_length=200,default='')

    def __str__(self):

        return self.payroll_id

tax_formula = '''24000=10%,8333=25%,467667=30%,300000=32.5%'''
class PayRollSetting(models.Model):
    
    org_name = models.CharField(max_length=100,default="")
    category = models.CharField(max_length=100)
    tax_rate = models.TextField(default=tax_formula)
    relief = models.FloatField(default=2400.00)
    nssf = models.FloatField()
    nhif = models.FloatField()
    health_insurance = models.FloatField(default=0.0)
    housing = models.FloatField(default=0.0)
    others = models.FloatField()

    def __str__(self):

        return self.category

    