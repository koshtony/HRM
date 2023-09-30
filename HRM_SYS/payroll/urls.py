from django.urls import path 
from . import views 
from .views import gen_payroll,monthly_payroll


urlpatterns = [
     
      path('reports',views.gen_payroll,name="payroll-reports"),
      path('monthly_payroll',views.monthly_payroll,name="payroll-month"),

]