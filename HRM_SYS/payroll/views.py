from django.shortcuts import render
from django.contrib import messages
from management.models import * 
from .formula import tax_amount
from .models import *
import pandas as pd
# Create your views here.


def gen_payroll(request):
    
    
    total_hours,expected_hours,deductions,leave_days,gross_pay,net_pay = 0,0,0,0,0,0
    payrolls = []
    for employee in Employee.objects.all():

        if len(Attendance.objects.filter(employee=employee)) > 0:
            
           
            for attendance in Attendance.objects.filter(employee=employee):

                 total_hours += attendance.hours
                 deductions += attendance.deductions 
                 leave_days += sum([leave.days for leave in Leave.objects.filter(applicant=User.objects.get(username=employee.emp_id)) if leave.status=="completed"])
                

            data = {
                "employee_id":employee.emp_id,
                "name":str(employee.first_name)+" "+ str(employee.second_name),
                "id_no":employee.national_no,
                "phone":employee.phone,
                "role":employee.role,
                "account_no":employee.account_no,
                "basic_salary":employee.salary,
                "allowance":employee.allowance,
                "add_ons":employee.add_ons,
                "total_hours":total_hours,
                "leave_days":leave_days,
                "deductions":deductions,
                "gross_pay":(employee.salary+employee.allowance+employee.add_ons)-deductions,
                "taxable_income":((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),
                "tax": tax_amount(employee.payroll_settings.tax_rate,((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),0),
                "nhif":employee.payroll_settings.nhif,
                "insurance":employee.payroll_settings.health_insurance,
                "housing": employee.payroll_settings.housing,
                "others": employee.payroll_settings.others,
                "net_pay": ((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf)\
                    -tax_amount(employee.payroll_settings.tax_rate,((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),0)\
                    -employee.payroll_settings.nhif-employee.payroll_settings.health_insurance-employee.payroll_settings.housing-employee.payroll_settings.others


            }
            payrolls.append(data)
            messages.success(request,'payment report created successfully')
        else:
            messages.error(request,'payment report created successfully')
    payrolls = pd.DataFrame(payrolls)
    print(payrolls)
    attendance = Attendance.objects.all()
    context = {"attendances":attendance,"payrolls":payrolls}
    return render(request,"payroll/reports.html",context)



