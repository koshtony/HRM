from django.urls import path 
from . import views 
from .views import home,clock,add_department,view_attendance,\
      add_roles,add_employee,add_info,approvals,list_employee,\
      view_approvals,Post,Event,leave,get_emp_files,get_attendance,\
      upload_leave,approve,upload_process,register,list_files,profile,EditEmpView,ResetPasswordView,\
      get_employee,reject_approval,approve_by_details,get_notify,departments,dep_details, recall_approval,recall_by_comment,\
            add_event,del_event,show_map,files_details,iframe_redirect,live_chat,live_chat_user,sent_msg,recv_msg,del_chat,chat_notify,chat_reply,\
            files_del,get_employee_template,import_employee_data,edit_att_settings,change_password,get_emp_other_details,view_approval_details,\
            resign_employee,employee_profile,create_approval,import_att_settings,lookup_employee,get_approval_temp

            

      

urlpatterns = [
     path('',views.home,name="management-home"),
     path('clock',views.clock,name="management-clock"),
     path('list_attendance',views.view_attendance,name="management_view_attendance"),
     path('get_attendance',views.get_attendance,name="management-get-attendance"),
     path('add_info',views.add_info,name="management_add_info"),
     path('add_departments',views.add_department,name="management_add_department"),
     path('add_roles',views.add_roles,name="management_add_roles"),
     path('add_employees',views.add_employee,name="management_add_employee"),
     path('resign_employees',views.resign_employee,name="management_resign_employee"),
     path('employee_profile/<str:id>',views.employee_profile,name="management_employee_profile"),
     path('approvals',views.approvals,name="management_approvals"),
      path('list_employee',views.list_employee,name="management_list_employee"),
       path('list_departments',views.departments,name="management_list_departments"),
       path('department_details/<str:name>',views.dep_details,name="management_departments_details"),
       path('get_employee',views.get_employee,name="management_get_employee"),
       path('import_employee_data',views.import_employee_data,name="management_import_employee_data"),
       path('lookup_employee',views.lookup_employee,name="management_lookup_employee"),
        path('import_att_settings',views.import_att_settings,name="management_import_att_settings"),
      path('get_files',views.get_employee,name="management_get_files"),
      path('get_emp_other_details',views.get_emp_other_details,name="management_get_emp_other_details"),
      path('files_details/<str:id>',views.files_details,name="management_files_details"),
      path('create_approval',views.create_approval,name="management_create_approval"),
      path('get_approval_template',views.get_approval_temp,name="management_get_approval_temp"),
      path('list_approvals',views.view_approvals,name="management_list_approvals"),
      path('view_approval_details',views.view_approval_details,name="management_view_approval_details"),
      path('leave',views.leave,name="management_leave"),
      path('upload_leave',views.upload_leave,name="management_upload_leave"),
      path('approve',views.approve,name="management_approve"),
      path('reject',views.reject_approval,name="management_reject"),
      path('approve_by_details',views.approve_by_details,name="management_approve_by_details"),
      path('recall_approval',views.recall_approval,name="management_recall_approval"),
      path('recall_by_comment',views.recall_by_comment,name="management_recall_by_comment"),
      path('upload_process',views.upload_process,name="management_upload_process"),
      path('events',views.Event,name="management_events"),
      path('add_event',views.add_event,name="management_add_event"),
      path('delete_event',views.del_event,name="management_del_event"),
      path('posts',views.Post,name="management_post"),
      path('register',views.register,name="management_register"),
      path('list_files',views.list_files,name="management_files"),
      path('del_files',views.files_del,name="management_del_files"),
      path('emp_temp',views.get_employee_template,name="management_emp_temp"),
      path('iframe_redirect',views.iframe_redirect,name="management_iframe_redirect"),
      path('profile',views.profile,name="management_profile"),
      path('get_notify',views.get_notify, name='management_get_notify'),
      path('chat_notify',views.chat_notify, name='management_chat_notify'),
      path('chat_reply',views.chat_reply, name='management_chat_reply'),
      path('live_chat',views.live_chat, name='management_live_chat'),
      path('live_chat/live_chat_user/<int:pk>',views.live_chat_user, name='management_live_chat_user'),
      path('live_chat/sent_msg/<int:pk>',views.sent_msg, name='management_sent_msg'),
      path('live_chat/recv_msg/<int:pk>',views.recv_msg, name='management_recv_msg'),
      path('del_chat',views.del_chat,name='chat-del'),
      path('edit_settings/<str:emp_id>',views.edit_att_settings,name='management-edit-settings'),
      path('show_map/<str:coords>',views.show_map, name='management_show_map'),
      path('edit_employee/<int:pk>',EditEmpView.as_view(),name="management-edit-employee"),
      path('change_password',views.change_password,name='change-password'),
      path('password-reset', ResetPasswordView.as_view(), name='password_reset'),

]