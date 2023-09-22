from django import forms 
from .models import Department,Roles,Employee,Applications,Leave

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

        model = Applications
        fields = ['type','details','remarks','attachment']

class LeaveForm(forms.ModelForm):

    class Meta:

        model = Leave
        fields = ['Approvals_type','category','start','end','attachments','remarks']