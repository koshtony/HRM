from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from management.models import * 
from .formula import tax_amount
from .models import *
import pandas as pd
# Create your views here.


def gen_payroll(request):
    
    

    attendance = Attendance.objects.all()
    payroll_report = PayRoll.objects.all()
    context = {"attendances":attendance,"payrolls":payroll_report}
    return render(request,"payroll/reports.html",context)

def monthly_payroll(request):
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        print(date1)
        
        payrolls = []
        payroll_id = hash(datetime.datetime.now())
        if payroll_id < 0:
            payroll_id = payroll_id*-1
        for employee in Employee.objects.all():
            
            attendances = Attendance.objects.filter(employee=employee).filter(created__range = [date1,date2])
            if len(attendances) > 0:
               
                total_hours,expected_hours,deductions,leave_days,gross_pay,net_pay,days = 0,0,0,0,0,0,0
                for attendance in attendances:

                    total_hours += attendance.hours
                    leave_days += sum([leave.days for leave in Leave.objects.filter(applicant=User.objects.get(username=employee.emp_id)) if leave.status=="completed"])
                    days += attendance.days
                    
                 
                data = {
                    "org_name":"",
                    "payroll_id":payroll_id,
                    "employee_id":employee.emp_id,
                    "sign_id":str(payroll_id)+str(employee.emp_id),
                    "name":str(employee.first_name)+" "+ str(employee.second_name),
                    "id_no":employee.national_no,
                    "pin_no":employee.kra_pin,
                    "phone":employee.phone,
                    "role":employee.role,
                    "account_no":employee.account_no,
                    "basic_salary":employee.salary,
                    "allowance":employee.allowance,
                    "add_ons":employee.add_ons,
                    "total_hours":total_hours,
                    "leave_days":leave_days,
                    "deductions":((AttSettings.objects.get(employee_id=employee.emp_id).expected_days)-days)*AttSettings.objects.get(employee_id=employee.emp_id).deduction_per_day,
                    "gross_pay":(employee.salary+employee.allowance+employee.add_ons)-deductions,
                    "taxable_income":((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),
                    "tax": tax_amount(employee.payroll_settings.tax_rate,((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),0),
                    "nhif":employee.payroll_settings.nhif,
                    "nssf":employee.payroll_settings.nssf,
                    "insurance":employee.payroll_settings.health_insurance,
                    "housing": employee.payroll_settings.housing,
                    "others": employee.payroll_settings.others,
                    "net_pay": ((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf)\
                        -tax_amount(employee.payroll_settings.tax_rate,((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),0)\
                        -employee.payroll_settings.nhif-employee.payroll_settings.health_insurance-employee.payroll_settings.housing-employee.payroll_settings.others,

                    "created": datetime.datetime.now()


                }
                payrolls.append(data)
                
            else:

                JsonResponse("no data to process",safe=False)
                
        print(payrolls)
        for payroll in payrolls:

            pay = PayRoll(**payroll)
            pay.save()

        return JsonResponse("successfully generated",safe=False)

def gen_payslip(request,signid):
    
    emp_payroll = PayRoll.objects.get(sign_id=signid)

    print(emp_payroll)

    context = {"details":emp_payroll}

    return render(request,'payroll/payslip.html',context)



    




    






