from django import forms
from .models import Voters

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Voters
        fields = ['Email', 'Username', 'Password']
