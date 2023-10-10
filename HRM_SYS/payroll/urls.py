from django.urls import path 
from . import views 
from .views import gen_payroll,monthly_payroll,gen_payslip,payroll_details,EditPayrollView


urlpatterns = [
     
      path('reports',views.gen_payroll,name="payroll-reports"),
      path('monthly_payroll',views.monthly_payroll,name="payroll-month"),
      path('payslip/<str:signid>',views.gen_payslip,name="payroll-payslip"),
      path('payroll_details',views.payroll_details,name="payroll-details"),
      path('edit_payroll/<int:pk>',EditPayrollView.as_view(),name="payroll-edit-payroll"),

]