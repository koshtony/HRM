from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.template.loader import render_to_string,get_template
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.db.models import Sum,Count
from management.models import * 
from .formula import tax_amount
from .models import *
import datetime
from datetime import datetime,date, timedelta
import pandas as pd
import json
from decimal import Decimal
import pytz
# Create your views here.


def gen_payroll(request):
    attendance = Attendance.objects.all()

    settings = PayRollSetting.objects.all()

    payroll_report = PayRoll.objects.all().order_by('-pk')

    grouped_payroll = PayRoll.objects.values('payroll_id').annotate(size = Count('employee_id'),total_amount=Sum('gross_pay'))

    context = {"attendances":attendance,"payrolls":payroll_report,"by_payroll_ids":grouped_payroll,"settings":settings}

    return render(request,"payroll/reports.html",context)

def monthly_payroll(request):
    utc=pytz.UTC
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        payroll_id = request.POST.get("payId")
        print(payroll_id)
        
        date2 = utc.localize(datetime.strptime(date2, '%Y-%m-%d')+timedelta(days=1))
        date1 = utc.localize(datetime.strptime(date1, '%Y-%m-%d'))
        
        
        payrolls = []
        for employee in Employee.objects.all():
            
            attendances = Attendance.objects.filter(employee=employee).filter(created__range = [date1,date2])
            if len(attendances) > 0:
               
                total_hours,expected_hours,deductions,leave_days,gross_pay,net_pay,days = 0,0,0,0,0,0,0
                for attendance in attendances:

                    total_hours += attendance.hours
                    
                    days += attendance.days
                leave_days += sum([leave.days for leave in Applications.objects.filter(applicant=User.objects.get(username=employee.emp_id)).filter(type__name = "leave") if leave.status=="complete"])
                overtime_hours = sum([i.overtime_hours for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2 ])
                overtime_pay = sum([(i.overtime_hours * i.overtime_rate) for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                incentives  = sum([i.incentive for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                loan_deductions = sum([i.loan_deductions for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                welfare_deductions = sum([i.welfare_deductions for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                deductions = Decimal(((AttSettings.objects.get(employee_id=employee.emp_id).expected_days)-days)*AttSettings.objects.get(employee_id=employee.emp_id).deduction_per_day)
                
                gross_pay = Decimal(Decimal(employee.salary)+Decimal(employee.allowance)+Decimal(employee.add_ons)+Decimal(incentives))+Decimal(overtime_pay)
        
                taxable_income  = Decimal(Decimal(gross_pay)-(employee.payroll_settings.nssf))
                tax =  Decimal(tax_amount(employee.payroll_settings.tax_rate,Decimal(gross_pay-employee.payroll_settings.nssf),employee.payroll_settings.relief))
                net_pay = round( Decimal((gross_pay))-(employee.payroll_settings.nssf)\
                        -round(tax,2)\
                        -employee.payroll_settings.nhif-employee.payroll_settings.health_insurance-employee.payroll_settings.housing-employee.payroll_settings.others-deductions-loan_deductions-welfare_deductions,2)
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
                    "overtime_pay":overtime_pay,
                    "overtime_hours":overtime_hours,
                    "incentives":incentives,
                    "add_ons":employee.add_ons,
                    "total_days":days,
                    "leave_days":leave_days,
                    "deductions":deductions,
                    "loan_deductions":loan_deductions,
                    "welfare_deductions":welfare_deductions,
                    "gross_pay":gross_pay,
                    "taxable_income":taxable_income,
                    "tax": tax,
                    "nhif":employee.payroll_settings.nhif,
                    "nssf":employee.payroll_settings.nssf,
                    "insurance":employee.payroll_settings.health_insurance,
                    "housing": employee.payroll_settings.housing,
                    "others": employee.payroll_settings.others,
                    "net_pay":net_pay,
                    
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

def email_payroll(request):

    if request.POST:

        payroll_id = request.POST.get("payroll_id")
        payrolls = PayRoll.objects.filter(payroll_id = payroll_id)
        
        for payroll in payrolls:

            subject = payrolls[0].org_name + " payroll "+payrolls[0].pay_run

            

            html_body = render_to_string("payroll/payslip.html",{ 'details': PayRoll.objects.get(sign_id=payroll.sign_id)} )

            message = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email="koshtech.site@gmail.com",
            to=[Employee.objects.get(emp_id = payroll.employee_id).email]
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)

        return JsonResponse("emailed successfully",safe=False)

            



def re_calculate(request):

    if request.POST:

        sign_id = request.POST.get("sign_id")
        org_name = request.POST.get("org_name")
        pin_no = request.POST.get("pin_no")
        basic_salary = Decimal(request.POST.get("basic_salary"))
        add_ons = Decimal(request.POST.get("add_ons"))
        total_days = Decimal(request.POST.get("total_hours"))
        leave_days = Decimal(request.POST.get("leave_days"))
        deductions = Decimal(request.POST.get("deductions"))
        nhif = Decimal(request.POST.get("nhif"))
        nssf = Decimal(request.POST.get("nssf"))
        insurance = Decimal(request.POST.get("insurance"))
        housing = Decimal(request.POST.get("housing"))
        others = Decimal(request.POST.get("others"))
        allowance = Decimal(request.POST.get("allowance"))
        overtime_pay = Decimal(request.POST.get("overtime_pay"))
        overtime_hours = Decimal(request.POST.get("overtime_hours"))
        incentives = Decimal(request.POST.get("incentives"))
        welfare = Decimal(request.POST.get("welfare"))
        loan  = Decimal(request.POST.get("loan"))
        
        gross_pay = basic_salary+allowance+overtime_pay+overtime_pay+add_ons
        taxable_income = gross_pay - nssf
        
        employee = Employee.objects.get(emp_id = PayRoll.objects.get(sign_id=sign_id).employee_id)
        
        filt_payroll = PayRoll.objects.get(sign_id = sign_id)
        filt_payroll.org_name = org_name
        filt_payroll.pin_no = pin_no 
        filt_payroll.basic_salary = basic_salary
        filt_payroll.total_days = total_days 
        filt_payroll.leave_days = leave_days 
        filt_payroll.deductions = deductions 
        filt_payroll.add_ons = add_ons 
        filt_payroll.nhif = nhif 
        filt_payroll.nssf = nssf 
        filt_payroll.insurance = insurance 
        filt_payroll.housing = housing
        filt_payroll.others = others
        filt_payroll.allowance = allowance
        filt_payroll.gross_pay = gross_pay
        filt_payroll.taxable_income = taxable_income
        filt_payroll.tax = tax_amount(employee.payroll_settings.tax_rate,taxable_income,employee.payroll_settings.relief)
        filt_payroll.net_pay = round(gross_pay-nssf\
                        -round(tax_amount(employee.payroll_settings.tax_rate,taxable_income,employee.payroll_settings.relief),2)\
                        -nhif-insurance-housing-others-welfare-loan,2)
        

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





    




    






