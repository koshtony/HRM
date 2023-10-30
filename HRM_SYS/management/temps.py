from .models import Employee
import pandas
def gen_temp(filename):
    emp_df = pandas.DataFrame(list(Employee.objects.all().values()))

    emp_df.to_excel(filename)