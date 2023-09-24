from django.urls import path 
from . import views 
from .views import gen_payroll


urlpatterns = [
     
      path('reports',views.gen_payroll,name="payroll-reports"),

]