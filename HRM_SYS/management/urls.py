from django.urls import path 
from . import views 
from .views import home,clock,add_department,\
      add_roles,add_employee,add_info,approvals,list_employee,\
      view_approvals,Post,Events,leave,get_emp_files,get_attendance,\
      upload_leave,approve,upload_process,register,list_files,profile,EditEmpView,ResetPasswordView
      

urlpatterns = [
     path('',views.home,name="management-home"),
     path('clock',views.clock,name="management-clock"),
     path('get_attendance',views.get_attendance,name="management-get-attendance"),
     path('add_info',views.add_info,name="management_add_info"),
     path('add_departments',views.add_department,name="management_add_department"),
     path('add_roles',views.add_roles,name="management_add_roles"),
     path('add_employees',views.add_employee,name="management_add_employee"),
     path('approvals',views.approvals,name="management_approvals"),
      path('list_employee',views.list_employee,name="management_list_employee"),
      path('get_files',views.get_emp_files,name="management_get_files"),
      path('list_approvals',views.view_approvals,name="management_list_approvals"),
      path('leave',views.leave,name="management_leave"),
      path('upload_leave',views.upload_leave,name="management_upload_leave"),
      path('approve',views.approve,name="management_approve"),
      path('upload_process',views.upload_process,name="management_upload_process"),
      path('events',views.Events,name="management_events"),
      path('posts',views.Post,name="management_post"),
      path('register',views.register,name="management_register"),
      path('list_files',views.list_files,name="management_files"),
       path('profile',views.profile,name="management_profile"),
        path('edit_employee/<int:pk>',EditEmpView.as_view(),name="management-edit-employee"),
        path('password-reset', ResetPasswordView.as_view(), name='password_reset')

]