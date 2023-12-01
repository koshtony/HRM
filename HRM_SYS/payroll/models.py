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
    basic_salary = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    allowance =  models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    add_ons = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    total_days = models.FloatField(default=0.0)
    overtime_hours = models.FloatField(default=0.0)
    overtime_pay = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    incentives = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    leave_days = models.FloatField(default=0.0)
    deductions = models.DecimalField(default=0.00,max_digits=10,decimal_places=2) 
    gross_pay  = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    taxable_income = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    tax = models.DecimalField(default=0.00,max_digits=10,decimal_places=2) 
    nhif = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    nssf = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    insurance = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    housing = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    loan_deductions = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    welfare_deductions = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    others = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    net_pay = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    created_date = models.DateField(default=timezone.now)
    created_time = models.TimeField(default=timezone.now)
    status = models.CharField(max_length=100,default="audit")
    pay_run = models.CharField(max_length=200,default='')
 

    def __str__(self):

        return self.payroll_id

tax_formula = '''24000=10,8333=25,467667=30,300000=32.5'''
class PayRollSetting(models.Model):
    
    org_name = models.CharField(max_length=100,default="")
    category = models.CharField(max_length=100)
    tax_rate = models.TextField(default=tax_formula)
    relief = models.DecimalField(default=2400.00,max_digits=10,decimal_places=2)
    nssf = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
   


    def __str__(self):

        return self.category

class ExtraPayments(models.Model):

    employee_id = models.CharField(max_length=100)
    overtime_hours = models.FloatField(default=0.0)
    overtime_rate = models.FloatField(default=0.0)
    incentive = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    performance = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    awards = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    loan_deductions = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    welfare_deductions = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    created = models.DateTimeField(default=timezone.now)


    def __str__(self):

        return self.employee_id

class Payroll_Rates(models.Model):

    nhif_rates_file = models.FileField(upload_to='nhif_files')
    nhif_relief_rate = models.FloatField(default=15.0)
    nssf_rate = models.FloatField(default=6.0)
    house_levy_rate = models.FloatField(default=1.5)
    paye_rates = models.FileField(upload_to='paye_files')
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return str(self.created)



