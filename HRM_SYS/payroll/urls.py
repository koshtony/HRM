from django.urls import path 
from . import views 
from .views import gen_payroll,monthly_payroll,gen_payslip


urlpatterns = [
     
      path('reports',views.gen_payroll,name="payroll-reports"),
      path('monthly_payroll',views.monthly_payroll,name="payroll-month"),
      path('payslip/<str:signid>',views.gen_payslip,name="payroll-payslip"),

]