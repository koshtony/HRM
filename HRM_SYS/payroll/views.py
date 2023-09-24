from django.shortcuts import render
from management.models import * 
from .models import *
# Create your views here.


def gen_payroll(request):
    employees = Employee.objects.all()
    leaves = Leave.objects.all()
    attendance = Attendance.objects.all()
    context = {"attendances":attendance}

    return render(request,"payroll/reports.html",context)

