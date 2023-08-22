from .models import Report, Account
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

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
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    org = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User  # Use the User model here
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            account = Account(user=user, organization=self.cleaned_data['org'])
            account.save()  # Create the associated Account
        return user

