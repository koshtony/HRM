from django.urls import path 
from . import views 
from .views import home,clock,add_department,add_roles,add_employee,add_info,approvals

urlpatterns = [
     path('home',views.home,name="management-home"),
     path('clock',views.clock,name="management-clock"),
     path('add_info',views.add_info,name="management_add_info"),
     path('add_departments',views.add_department,name="management_add_department"),
     path('add_roles',views.add_roles,name="management_add_roles"),
     path('add_employees',views.add_employee,name="management_add_employee"),
     path('approvals',views.approvals,name="management_approvals"),

]