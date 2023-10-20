from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.db.models import Sum,Count
from management.models import * 
from .formula import tax_amount
from .models import *
import datetime
from datetime import datetime,date, timedelta
import pandas as pd
import json
# Create your views here.


def gen_payroll(request):
    attendance = Attendance.objects.all()

    settings = PayRollSetting.objects.all()

    payroll_report = PayRoll.objects.all().order_by('-pk')

    grouped_payroll = PayRoll.objects.values('payroll_id').annotate(size = Count('employee_id'),total_amount=Sum('gross_pay'))

    context = {"attendances":attendance,"payrolls":payroll_report,"by_payroll_ids":grouped_payroll,"settings":settings}

    return render(request,"payroll/reports.html",context)

def monthly_payroll(request):
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        payroll_id = request.POST.get("payId")
        print(payroll_id)
        
        date2 = datetime.strptime(date2, '%Y-%m-%d')+timedelta(days=1)
        
        
        payrolls = []
        for employee in Employee.objects.all():
            
            attendances = Attendance.objects.filter(employee=employee).filter(created__range = [date1,date2])
            if len(attendances) > 0:
               
                total_hours,expected_hours,deductions,leave_days,gross_pay,net_pay,days = 0,0,0,0,0,0,0
                for attendance in attendances:

                    total_hours += attendance.hours
                    leave_days += sum([leave.days for leave in Applications.objects.filter(applicant=User.objects.get(username=employee.emp_id)).filter(type__name = "leave") if leave.status=="complete"])
                    days += attendance.days
                    
                 
                data = {
                    "org_name":employee.payroll_settings.org_name,
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
                    "total_hours":days,
                    "leave_days":leave_days,
                    "deductions":round(((AttSettings.objects.get(employee_id=employee.emp_id).expected_days)-days)*AttSettings.objects.get(employee_id=employee.emp_id).deduction_per_day,2),
                    "gross_pay":round((employee.salary+employee.allowance+employee.add_ons)-deductions,2),
                    "taxable_income":round(((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),2),
                    "tax": round(tax_amount(employee.payroll_settings.tax_rate,((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),employee.payroll_settings.relief),2),
                    "nhif":employee.payroll_settings.nhif,
                    "nssf":employee.payroll_settings.nssf,
                    "insurance":employee.payroll_settings.health_insurance,
                    "housing": employee.payroll_settings.housing,
                    "others": employee.payroll_settings.others,
                    "net_pay":round( ((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf)\
                        -round(tax_amount(employee.payroll_settings.tax_rate,((employee.salary+employee.allowance+employee.add_ons)-deductions)-(employee.payroll_settings.nssf),employee.payroll_settings.relief),2)\
                        -employee.payroll_settings.nhif-employee.payroll_settings.health_insurance-employee.payroll_settings.housing-employee.payroll_settings.others,2),

                    "created_date": datetime.now(),
                    "created_time":datetime.now(),
                    "pay_run": str(date1)+" - "+str(date2)
                    


                }
                payrolls.append(data)
                
            else:

                JsonResponse("no data to process",safe=False)
                
        print(payrolls)
        for payroll in payrolls:

            pay = PayRoll(**payroll)
            pay.save()

        return JsonResponse(json.dumps(payrolls,default=str),safe=False)

def gen_payslip(request,signid):
    
    emp_payroll = PayRoll.objects.get(sign_id=signid)

  

    context = {"details":emp_payroll}

    return render(request,'payroll/payslip.html',context)


def payroll_details(request):

    if request.POST:

        id = request.POST.get("id")
    
        details = PayRoll.objects.filter(payroll_id=id)
        
        cost,size,org= 0,0,[]
        payrolls,created = [],[]
        for detail in details:

            info = {
                "employee_id":detail.employee_id,
                "name":detail.name,
                "pin_no":detail.pin_no,
                "taxable":detail.taxable_income,
                "gross_pay":detail.gross_pay,
                "paye":detail.tax,
                "net_pay":detail.net_pay,
                "created":detail.created_date,
            }
            cost+=detail.gross_pay
            size+=1
            org.append(detail.org_name)
            created.append(detail.created_date)

           

            payrolls.append(info)
        summary = {"cost":cost,"size":size,"org":org,"created":created[0]}
        print(summary)
        return JsonResponse(json.dumps(summary,default=str),safe=False)
    
def payroll_check(request):

    if request.POST:

        id = request.POST.get("id")
        print(id)

        payrolls = PayRoll.objects.filter(payroll_id = id)
        for payroll in payrolls:

            payroll.status = "audited"

            payroll.save()

        return JsonResponse("audit completed",safe=False)


'''  
    ===================================================================================
        create view where payroll master can change info manually
'''

def grouped_payroll(request):

    grouped_payroll = PayRoll.objects.values('payroll_id').annotate(size = Count('employee_id'),total_amount=Sum('gross_pay'))

    context = {"by_payroll_ids":grouped_payroll}

    return render(request,'payroll/grouped_table.html',context)


def re_calculate(request):

    if request.POST:

        sign_id = request.POST.get("sign_id")
        org_name = request.POST.get("org_name")
        pin_no = request.POST.get("pin_no")
        basic_salary = float(request.POST.get("basic_salary"))
        add_ons = float(request.POST.get("add_ons"))
        total_hours = float(request.POST.get("total_hours"))
        leave_days = float(request.POST.get("leave_days"))
        deductions = float(request.POST.get("deductions"))
        nhif = float(request.POST.get("nhif"))
        nssf = float(request.POST.get("nssf"))
        insurance = float(request.POST.get("insurance"))
        housing = float(request.POST.get("housing"))
        others = float(request.POST.get("others"))
        allowance = float(request.POST.get("allowance"))
        
        employee = Employee.objects.get(emp_id = PayRoll.objects.get(sign_id=sign_id).employee_id)
        
        filt_payroll = PayRoll.objects.get(sign_id = sign_id)
        filt_payroll.org_name = org_name
        filt_payroll.pin_no = pin_no 
        filt_payroll.basic_salary = basic_salary
        filt_payroll.total_hours = total_hours 
        filt_payroll.leave_days = leave_days 
        filt_payroll.deductions = deductions 
        filt_payroll.add_ons = add_ons 
        filt_payroll.nhif = nhif 
        filt_payroll.nssf = nssf 
        filt_payroll.insurance = insurance 
        filt_payroll.housing = housing
        filt_payroll.others = others
        filt_payroll.allowance = allowance
        filt_payroll.gross_pay = round((basic_salary+allowance+add_ons)-deductions,2)
        filt_payroll.taxable_income = round(((basic_salary+allowance+add_ons)-deductions)-(nssf),2)
        filt_payroll.tax = round(tax_amount(employee.payroll_settings.tax_rate,((basic_salary+allowance+add_ons)-deductions)-(nssf),employee.payroll_settings.relief),2)
        filt_payroll.net_pay = round(((basic_salary+allowance+add_ons)-deductions)-(nssf)\
                        -round(tax_amount(employee.payroll_settings.tax_rate,((basic_salary+allowance+add_ons)-deductions)-(nssf),employee.payroll_settings.relief),2)\
                        -nhif-insurance-housing-others,2)
        

        filt_payroll.status = "audited"
        filt_payroll.created_date = datetime.now()
        filt_payroll.created_time = datetime.now()
        

        filt_payroll.save()




        return JsonResponse("done calculating",safe=False)
# class views


class EditPayrollView(LoginRequiredMixin,UpdateView):

    model = PayRoll 
    template_name = 'payroll/edit_payroll.html'
    fields = '__all__'
    raise_exception = True
    success_url = '/iframe_redirect'





    




    






