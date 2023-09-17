from django import forms 
from .models import Department,Roles,Employee,Approvals

class DepForm(forms.ModelForm):

    class Meta:

        model = Department
        fields = '__all__'

class RoleForm(forms.ModelForm):

    class Meta:

        model = Roles
        fields = '__all__'

class EmpForm(forms.ModelForm):

    class Meta:

        model = Employee
        fields = '__all__'


class ApprovalForm(forms.ModelForm):

    class Meta:

        model = Approvals
        fields = '__all__'