from django import forms 
from .models import ExtraPayments 

class ExtraPaymentsForm(forms.ModelForm):

    class Meta:

        model = ExtraPayments 
        fields = "__all__"

