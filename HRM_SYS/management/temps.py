from .models import Employee,AttSettings,Attendance
import pandas
def gen_temp(filename):
    emp_df = pandas.DataFrame(list(Employee.objects.all().values()))
    AttSettings_df = pandas.DataFrame(list(AttSettings.objects.all().values()))

    with pandas.ExcelWriter(filename) as writer:  
        emp_df.to_excel(writer, sheet_name='employee',index=False),
        AttSettings_df.to_excel(writer, sheet_name='attendance',index=False)

def emp_attendance(filename):

    att_df = pandas.DataFrame(list(Attendance.objects.all().values()))

    with pandas.ExcelWriter(filename) as writer:  
        att_df.to_excel(writer, sheet_name='attendance',index=False),



