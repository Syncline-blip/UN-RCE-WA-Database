from django import forms
from .models import Report

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
