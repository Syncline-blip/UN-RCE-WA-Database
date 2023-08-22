from django import forms
from .models import Report
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'lead_organisation', 
            'name_project', 
            'project_description', 
            'delivery', 
            'frequency', 
            'audience', 
            'current_partners', 
            'sdg_focus', 
            'contact',
        ]
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "name", "lastName", "org") 

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit: user.save()
            return user

