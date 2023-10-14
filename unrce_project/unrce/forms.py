from .models import Report, Account, ReportImages, Organization, ReportFiles,  AUDIENCE_CHOICES, DELIVERY_CHOICES, INDUSTRY_CHOICES, PROFILE_SDG_CHOICES 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from zxcvbn import zxcvbn  # Import the zxcvbn library
from django.core.validators import MinLengthValidator
from .models import Account



class DateInput(forms.DateInput):
    input_type = 'date'


class ReportForm(forms.ModelForm):

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
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['frequency'].required = False
        self.fields['region'].required = False

    class Meta:
        model = Report
        widgets = {
            'start_project': DateInput(),
            'end_project': DateInput(),
        }
        exclude = ['author', 'created_at', 'last_modified', 'contributing_organisations', 'direct_sdgs', 'indirect_sdgs', 'approved','direct_esd_themes','indirect_esd_themes','direct_priority_areas', 'indirect_priority_areas', 'submitted'   ]

class ReportImagesForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = ReportImages
        fields = ['image']

class ReportFilesForm(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = ReportFiles
        fields = ['file']

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'email', 'website']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    org = forms.CharField(max_length=100, required=True)

    # Add MinLengthValidator with custom error messages for username and password
    username = forms.CharField(
        validators=[
            MinLengthValidator(limit_value=5, message="Username must be at least 5 characters long."),
        ]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters long and contain at least one uppercase letter, one special character, and one number."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            account = Account(user=user, organization=self.cleaned_data['org'])
            account.save() 
        return user

    "Validate the password"
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1:
            # Use zxcvbn to evaluate password strength
            result = zxcvbn(password1)
            if result['score'] < 3:
                raise forms.ValidationError(
                    "Password is too weak. Please choose a stronger password."
                )
        return password1
    
OrganizationInlineFormSet = forms.inlineformset_factory(
    Report,
    Organization,
    fields=('name', 'email', 'website'),
    extra=3,   
    can_delete=True
)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['organization', 'profile_sdg', 'sector', 'message']
        exclude =['approved']

    profile_sdg = forms.MultipleChoiceField(
        choices=PROFILE_SDG_CHOICES , 
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
