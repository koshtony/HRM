from django.urls import path 
from . import views 
from .views import home,clock,add_department,\
      add_roles,add_employee,add_info,approvals,list_employee,\
      view_approvals,Post,Events,leave

urlpatterns = [
     path('',views.home,name="management-home"),
     path('clock',views.clock,name="management-clock"),
     path('add_info',views.add_info,name="management_add_info"),
     path('add_departments',views.add_department,name="management_add_department"),
     path('add_roles',views.add_roles,name="management_add_roles"),
     path('add_employees',views.add_employee,name="management_add_employee"),
     path('approvals',views.approvals,name="management_approvals"),
      path('list_employee',views.list_employee,name="management_list_employee"),
      path('list_approvals',views.view_approvals,name="management_list_approvals"),
      path('leave',views.leave,name="management_leave"),
      path('events',views.Events,name="management_events"),
      path('posts',views.Post,name="management_post"),

]