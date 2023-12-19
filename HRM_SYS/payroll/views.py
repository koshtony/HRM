from django.shortcuts import render
from django.http import JsonResponse,FileResponse
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.template.loader import render_to_string,get_template
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.db.models import Sum,Count
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from .forms import ExtraPaymentsForm
from management.models import * 
from .formula import tax_amount,nhif_pay,nssf_pay,house_levy_pay,nhif_relief
from .temps import gen_temp
from .models import *
import datetime
from datetime import datetime,date, timedelta
import pandas as pd
import json
from decimal import Decimal

import math
import pytz
import os
# Create your views here.


def gen_payroll(request):
    attendance = Attendance.objects.all()

    settings = PayRollSetting.objects.all()

    payroll_report = PayRoll.objects.all().order_by('-pk')

    grouped_payroll = PayRoll.objects.values('payroll_id').annotate(size = Count('employee_id'),total_amount=Sum('gross_pay'))

    context = {"attendances":attendance,"payrolls":payroll_report,"by_payroll_ids":grouped_payroll,"settings":settings,"extra_payment_form":ExtraPaymentsForm}

    return render(request,"payroll/reports.html",context)

def monthly_payroll(request):
    utc=pytz.UTC
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        payroll_id = request.POST.get("payId")
      
        
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
                if str(overtime_pay).isdecimal()==False:
                    overtime_pay = 0.00
                incentives  = sum([i.incentive for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                if str(incentives).isdecimal() ==False:
                    incentives = 0.00
                loan_deductions = sum([i.loan_deductions for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                if str(loan_deductions).isdecimal() == False:
                    loan_deductions = 0.00
                welfare_deductions = sum([i.welfare_deductions for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
                if str(welfare_deductions).isdecimal == False:
                    welfare_deductions == 0.00
                try:
                    deductions = Decimal(((AttSettings.objects.get(employee_id=employee.emp_id).expected_days)-days)*AttSettings.objects.get(employee_id=employee.emp_id).deduction_per_day)
                except:
                    deductions = 0.00
                
                if math.isnan(employee.salary)==True:
                    gross_pay = Decimal(0.00+Decimal(incentives))+Decimal(overtime_pay)
                
                else:
                    gross_pay = Decimal(employee.salary+incentives+overtime_pay)

                nhif = nhif_pay(gross_pay)

                nssf = employee.payroll_settings.nssf

                house_levy = house_levy_pay(gross_pay)
        
                taxable_income  = Decimal(Decimal(gross_pay)-(nssf))

                tax =  Decimal(tax_amount(employee.payroll_settings.tax_rate,taxable_income,employee.payroll_settings.relief))
                
                nhif_relf = Decimal(nhif_relief(nhif,tax))

                net_pay = gross_pay-Decimal(nssf)\
                        -tax-nhif_relf\
                        -Decimal(nhif)-Decimal(house_levy)-Decimal(deductions)-Decimal(loan_deductions)-Decimal(welfare_deductions)
                
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
                    "nhif":nhif,
                    "nssf":nssf,
                    
                    "housing": house_levy,
                   
                    "net_pay":net_pay,
                    
                    "created_date": datetime.now(),
                    "created_time":datetime.now(),
                    "pay_run": str(date1)+" - "+str(date2)
                    


                }
                payrolls.append(data)
           
                
            else:

                JsonResponse("no data to process",safe=False)
                
   
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
       
        return JsonResponse(json.dumps(summary,default=str),safe=False)
    
def payroll_check(request):

    if request.POST:

        id = request.POST.get("id")
     

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

def payroll_sum(request,payroll_id):
    
    filtered = PayRoll.objects.filter(payroll_id = payroll_id)
    summary = filtered.values('payroll_id')\
              .annotate(
                  size = Count('employee_id'),salary = Sum('basic_salary'),allowance = Sum('allowance'),add_ons = Sum('add_ons'),
                  overtime = Sum('overtime_pay'),incentives = Sum('incentives'),
                  deductions = Sum('deductions'),gross = Sum('gross_pay'),tax=Sum('tax'),
                  nhif = Sum('nhif'),nssf = Sum('nssf'),insurance = Sum('insurance'),housing = Sum('housing'),loan = Sum('loan_deductions'),
                  welfare = Sum('welfare_deductions'),others = Sum('others')
                        
                        
                        )
 
    context = {"summary":summary[0],"payrun":filtered[0].pay_run,"org":filtered[0].org_name}
    
    return render(request,'payroll/summary.html',context)

def add_extra_payments(request):

    if request.POST:

        form = ExtraPaymentsForm(request.POST)

        if form.is_valid():

            form.save()

            return JsonResponse("details submitted successfully",safe=False)

def gen_extra_payement_temp(request):

    filename = 'extra_payments_template.xlsx'

    filepath =  os.path.join(settings.MEDIA_ROOT, 'extra_payments_temp',filename)
    gen_temp(filepath)

    path = open(filepath,'rb')

    response = FileResponse(path,as_attachment=True)

    return response
@csrf_exempt
def import_extra_payments(request):

    try:

        file = request.FILES.get("file")
        extra_df = pd.read_excel(file)
        for items in extra_df.to_dict("records"):

            extra = ExtraPayments(
                **items
            )
            extra.save()
        return JsonResponse("file processed successfully",safe=False)
    except Exception as err:

        return JsonResponse(str(err),safe=False)

def flat_payroll(request):
    utc=pytz.UTC
    if request.POST:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        payroll_id = request.POST.get("payId")
        
            
        date2 = utc.localize(datetime.strptime(date2, '%Y-%m-%d')+timedelta(days=1))
        date1 = utc.localize(datetime.strptime(date1, '%Y-%m-%d'))
        all_payrolls = []
        for employee in Employee.objects.all():

            
            overtime_hours = sum([i.overtime_hours for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2 ])
            overtime_pay = sum([(i.overtime_hours * i.overtime_rate) for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
            if str(overtime_pay).isdecimal()==False:
                overtime_pay = 0.00
            incentives  = sum([i.incentive for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
            if str(incentives).isdecimal() ==False:
                incentives = 0.00
            loan_deductions = sum([i.loan_deductions for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
            if str(loan_deductions).isdecimal() == False:
                loan_deductions = 0.00
            welfare_deductions = sum([i.welfare_deductions for i in ExtraPayments.objects.filter(employee_id = employee.emp_id) if i.created >= date1 and i.created <= date2])
            if str(welfare_deductions).isdecimal == False:
                welfare_deductions == 0.00
            deductions = 0.00
            
            
           
            
            if math.isnan(employee.salary)==True:
                salary = 0.00
                gross_pay = Decimal(0.00+incentives+overtime_pay)
            else:
                salary = employee.salary
                gross_pay = Decimal(employee.salary+incentives+overtime_pay)
            
            nhif = nhif_pay(gross_pay)


            nssf = employee.payroll_settings.nssf

            house_levy = house_levy_pay(gross_pay)

            taxable_income  = Decimal(Decimal(gross_pay)-(nssf))
            tax =  Decimal(tax_amount(employee.payroll_settings.tax_rate,taxable_income,employee.payroll_settings.relief))

            nhif_relf = Decimal(nhif_relief(nhif,tax))
            
            net_pay = gross_pay-Decimal(nssf)\
                            -tax-nhif_relf\
                            -Decimal(nhif)-Decimal(house_levy)-Decimal(deductions)-Decimal(loan_deductions)-Decimal(welfare_deductions)
      
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
                        "basic_salary":salary,
                        #"allowance":employee.allowance,
                        "overtime_pay":overtime_pay,
                        "overtime_hours":overtime_hours,
                        "incentives":incentives,
                        #"add_ons":employee.add_ons,
                        "total_days":24,
                        
                        "deductions":deductions,
                        "loan_deductions":loan_deductions,
                        "welfare_deductions":welfare_deductions,
                        "gross_pay":gross_pay,
                        "taxable_income":taxable_income,
                        "tax": tax,
                        "nhif":nhif,
                        "nssf":nssf,
                       
                        "housing": house_levy,
                        
                        "net_pay":net_pay,
                        
                        "created_date": datetime.now(),
                        "created_time":datetime.now(),
                        "pay_run": str(date1)+" - "+str(date2)
                        


                    }
            all_payrolls.append(data)
        
        for payroll in all_payrolls:

            pay = PayRoll(**payroll)
            pay.save()

        return JsonResponse(json.dumps(all_payrolls,default=str),safe=False)


def grouping(request):

    if request.POST:

        range1 = request.POST.get("range1")
        range2 = request.POST.get("range2")
        group = request.POST.get("group")

        emp_filts = Employee.objects.filter(salary__gte = range1).filter(salary__lte = range2)

        for emp_filt in emp_filts:
            print(emp_filt)
            emp_filt.payroll_settings = PayRollSetting.objects.get(category=group)
            emp_filt.save()

        return JsonResponse(str(range1)+" to "+str(range2)+" set to group1",safe=False)




class EditPayrollView(LoginRequiredMixin,UpdateView):

    model = PayRoll 
    template_name = 'payroll/edit_payroll.html'
    fields = '__all__'
    raise_exception = True
    success_url = '/iframe_redirect'





    




    






