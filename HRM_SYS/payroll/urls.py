from django.urls import path 
from . import views 
from .views import gen_payroll,monthly_payroll,gen_payslip,payroll_details,\
      payroll_check,grouped_payroll,EditPayrollView,re_calculate,email_payroll,\
            payroll_sum,add_extra_payments,gen_extra_payement_temp,import_extra_payments,flat_payroll,grouping,payroll_action


urlpatterns = [
     
      path('reports',views.gen_payroll,name="payroll-reports"),
      path('monthly_payroll',views.monthly_payroll,name="payroll-month"),
      path('flat_payroll',views.flat_payroll,name="payroll-flat"),
      path('payslip/<str:signid>',views.gen_payslip,name="payroll-payslip"),
      path('payroll_details',views.payroll_details,name="payroll-details"),
      path('payroll_check',views.payroll_check,name="payroll-check"),
      path('payroll_action',views.payroll_action,name="payroll-action"),
      path('payroll_re_calculate',views.re_calculate,name="payroll-re-calculate"),
      path('grouped_payroll',views.grouped_payroll,name="payroll-grouped"),
      path('grouping_payroll',views.grouping,name="payroll-grouping"),
      path('email_payroll',views.email_payroll,name="payroll-email"),
      path('add_extra_payments',views.add_extra_payments,name="payroll-extra-payments"),
      path('extra_payments_template',views.gen_extra_payement_temp,name="payroll-extra-payments-temp"),
      path('import_extra_payments',views.import_extra_payments,name="payroll-extra-payments-import"),
      path('summary/<str:payroll_id>',views.payroll_sum,name="payroll-summary"),
      path('edit_payroll/<int:pk>',EditPayrollView.as_view(),name="payroll-edit-payroll"),

]