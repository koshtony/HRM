from django.shortcuts import render
from django.http import JsonResponse
from .forms import EmpForm,ApprovalForm
# Create your views here.
def home(request):

    return render(request,'management/index.html')

def add_info(request):

    return render(request,'management/add_info.html')

def approvals(request):
    context = {"appForm":ApprovalForm}
    return render(request,'management/approvals.html',context)



def add_department(request):

    pass

def add_roles(request):

    pass

def add_employee(request):

    context = {"emp_form":EmpForm()}

    return render(request,'management/add_employees.html',context)

def clock(request):

    if request.POST:

        lat = request.POST.get('latitudes')
        long = request.POST.get('longitudes')
        image_info = request.POST.get('image_str')
        print(image_info)

        return JsonResponse("info submitted",safe=False)

    return render(request,'management/clock.html')