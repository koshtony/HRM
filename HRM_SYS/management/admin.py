from django.contrib import admin
from .models import Employee,Department,Roles,Approvals,\
Applications,Attendance,AttSettings,EmpFiles,FilesCategory,Leave,Profile

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
class ApprovalsAdmin(admin.ModelAdmin):
        list_display = ("name","created","get_approvers","remarks")
        search_fields = ["name"]

        def get_approvers(self,obj):

                return ",".join([str(app.approvers) for app in Approvals.objects.all()])



class ApplicationsAdmin(admin.ModelAdmin):
        list_display = ("type","details","created","attachment")
        list_filter = ("type",)
        search_fields = ["approvers"]

class AttAdmin(admin.ModelAdmin):
        list_display = ("employee","clock_in","clock_out","lat","long","lat1","long1","image1","image2")
        list_filter = ("employee",)
        
class FilesAdmin(admin.ModelAdmin):

        list_display = ("employee","category","properties","created","document")
        list_filter = ("employee",)


        


admin.site.register(Employee,EmpAdmin)
admin.site.register(Department,DepAdmin)
admin.site.register(Roles,RolesAdmin)
admin.site.register(Approvals,ApprovalsAdmin)
admin.site.register(Applications,ApplicationsAdmin)
admin.site.register(Attendance,AttAdmin)
admin.site.register(EmpFiles,FilesAdmin)
admin.site.register(AttSettings)
admin.site.register(FilesCategory)
admin.site.register(Leave)
admin.site.register(Profile)

