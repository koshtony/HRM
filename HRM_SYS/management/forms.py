from django import forms 
from .models import Department,Roles,Employee,Applications,Leave,Process,Profile,EmpFiles
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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

        model = Process
        fields = ['approvals','details','attachments']

class LeaveForm(forms.ModelForm):

    class Meta:

        model = Leave
        fields = ['Approvals_type','category','start','end','days','attachments','details']

class filesForm(forms.ModelForm):

    class Meta:

        model = EmpFiles
        fields = "__all__"

class profileForm(forms.ModelForm):

    class Meta:

        model = Profile 
        fields = '__all__'


class UserRegForm(UserCreationForm):
    email= forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User 
        fields = ['username','email']