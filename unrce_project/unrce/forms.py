# Django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Third-party imports
from zxcvbn import zxcvbn 

# Local application/library specific imports
from .models import (
    Account, AUDIENCE_CHOICES, DELIVERY_CHOICES, Expression_of_interest,
    INDUSTRY_CHOICES, Organization, PROFILE_SDG_CHOICES, Report,
    ReportFiles, ReportImages
)


class DateInput(forms.DateInput):
    input_type = 'date'


class ReportForm(forms.ModelForm):
    """Form for creating and editing reports"""

    # Multi-choice fields with Checkbox widgets
    audience = forms.MultipleChoiceField(
        choices=AUDIENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    delivery = forms.MultipleChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Making some fields non-mandatory
        self.fields['frequency'].required = False
        self.fields['region'].required = False

    class Meta:
        model = Report
        widgets = {'start_project': DateInput(), 'end_project': DateInput()}
        exclude = [
            'author', 'created_at', 'last_modified', 'contributing_organisations',
            'direct_sdgs', 'indirect_sdgs', 'approved', 'direct_esd_themes',
            'indirect_esd_themes', 'direct_priority_areas', 'indirect_priority_areas',
            'submitted'
        ]


class ReportImagesForm(forms.ModelForm):
    """Form for uploading report images"""

    image = forms.ImageField(required=False)

    class Meta:
        model = ReportImages
        fields = ['image']


class ReportFilesForm(forms.ModelForm):
    """Form for uploading report files"""

    file = forms.FileField(required=False)

    class Meta:
        model = ReportFiles
        fields = ['file']


class OrganizationForm(forms.ModelForm):
    """Form for organization details"""

    class Meta:
        model = Organization
        fields = ['name', 'email', 'website']


class InterestForm(forms.ModelForm):
    """Form for expressing interest"""

    class Meta:
        model = Expression_of_interest
        exclude = ['author']


class RegistrationForm(UserCreationForm):
    """User registration form with extended fields and custom validations"""

    # Extending the user creation form fields
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    org = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")

    def clean_password1(self):
        """Validates the strength of the password"""
        password1 = self.cleaned_data.get("password1")
        if password1:
            result = zxcvbn(password1)
            if result['score'] < 3:
                raise forms.ValidationError("Password is too weak. Please choose a stronger password.")
        return password1

    def save(self, commit=True):
        """Overrides the save method to add extended fields data"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Account(user=user, organization=self.cleaned_data['org']).save()
        return user


# Inline formset for organization - allows multiple organizations to be entered
OrganizationInlineFormSet = forms.inlineformset_factory(
    Report, Organization, fields=('name', 'email', 'website'), extra=3, can_delete=True
)


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class AccountUpdateForm(forms.ModelForm):
    """Form for updating account information"""

    class Meta:
        model = Account
        fields = ['organization']


class AccountForm(forms.ModelForm):
    """Form for account information with multiple choice fields"""

    profile_sdg = forms.MultipleChoiceField(
        choices=PROFILE_SDG_CHOICES, 
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sector = forms.ChoiceField(
        choices=INDUSTRY_CHOICES,
        widget=forms.Select,
        required=False
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'Message', 'rows': '4'}),
        max_length=200,
        required=True
    )

    class Meta:
        model = Account
        fields = ['organization', 'profile_sdg', 'sector', 'message']
        exclude =['approved']


class EditProfileForm(forms.ModelForm):
    """Form for editing profile with optional password change"""

    new_password = forms.CharField(required=False, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
