from django.contrib import admin
from .models import Employee,Department,Roles,Approvals,Approvers,Attendance

# Register your models here.

class EmpAdmin(admin.ModelAdmin):
        list_display = ("emp_id","first_name","second_name","email","phone","dob")
        list_filter = ("department",)
        search_fields = ["empid"]

class DepAdmin(admin.ModelAdmin):
        list_display = ("name","hod","size","created","remarks")
        list_filter = ("name",)
        search_fields = ["hod"]

class RolesAdmin(admin.ModelAdmin):
        list_display = ("name","requirements","created","remarks")
        list_filter = ("requirements",)
        search_fields = ["name"]
class ApproversAdmin(admin.ModelAdmin):
        list_display = ("Employee_ids","approval_type","created","remarks")
        list_filter = ("approval_type",)
        search_fields = ["Employee_ids"]

class ApprovalAdmin(admin.ModelAdmin):
        list_display = ("type","approvers","level","created","remarks")
        list_filter = ("type",)
        search_fields = ["level"]

class AttAdmin(admin.ModelAdmin):
        list_display = ("employee","clock_in","clock_out","lat","long","lat1","lat2","image1","image2")
        list_filter = ("employee",)
        

        


admin.site.register(Employee,EmpAdmin)
admin.site.register(Department,DepAdmin)
admin.site.register(Roles,RolesAdmin)
admin.site.register(Approvers,ApproversAdmin)
admin.site.register(Approvals,ApprovalAdmin)
admin.site.register(Attendance,AttAdmin)

