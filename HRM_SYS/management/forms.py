from django import forms 
from .models import Department,Roles,Employee,Applications,Leave,Process,Profile,EmpFiles,ChatMessage,Events,AttSettings,Approvals
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE


class DateInput(forms.DateInput):
    input_type = 'date'
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

class EmpUpdateForm(forms.ModelForm):

    class Meta:

        model = Employee 
        fields = '__all__'


class ApprovalForm(forms.ModelForm):
    details = forms.CharField(widget=TinyMCE(
            attrs={'required': False, 'cols': 5, 'rows': 5})
    )
    class Meta:

        model = Process
        fields = ['approvals','details','attachments']

class CreateApprovalForm(forms.ModelForm):
    template = forms.CharField(widget=TinyMCE(
            attrs={'cols': 15, 'rows': 5})
    )
    class Meta:

        model = Approvals
        fields = '__all__'


class LeaveForm(forms.ModelForm):

    class Meta:

        model = Leave
        fields = ['Approvals_type','category','start','end','days','remaining_leave_days','work_assignment','attachments','details']
        widgets = {
            'start': DateInput(),
            'end': DateInput(),
            'Approvals_type': forms.Select(attrs={'class': 'form-select'})

        }
        

class filesForm(forms.ModelForm):

    class Meta:

        model = EmpFiles
        fields = "__all__"
        
    

class profileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile 
        fields = ['image','first','email','surname','phone','activation']


class UserRegForm(UserCreationForm):
    email= forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=["username","email"]


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User 
        fields = ['username','email']

class ChatForm(forms.ModelForm):

    body = forms.CharField(widget=TinyMCE(
            attrs={'required': False, 'cols': 5, 'rows': 2})
    )
    
    class Meta:
        
        model = ChatMessage
        fields = [
            
            "body",
        ]

class PostsForm(forms.ModelForm):

    class Meta:

        model = Events 
        fields = ['title','details','files','category','viewers']

class SettingsForm(forms.ModelForm):

    class Meta:

        model = AttSettings
        fields = '__all__'
       