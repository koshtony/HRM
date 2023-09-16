from django.shortcuts import render

# Create your views here.
def home(request):

    return render(request,'management/index.html')

def add_info(request):

    return render(request,'management/add_info.html')

def add_department(request):

    pass

def add_roles(request):

    pass

def add_employee(request):

    pass

def clock(request):

    return render(request,'management/clock.html')