from .models import Report, Account, ExcelUpload, ReportImages, Expression_of_interest
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from zxcvbn import zxcvbn  # Import the zxcvbn library
from django.core.validators import MinLengthValidator

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['author']
        
class InterestForm(forms.ModelForm):
    class Meta:
        model = Expression_of_interest
        fields = '__all__'
        exclude = ['author']

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
    
class ExcelForm(forms.ModelForm):
    class Meta:
        model = ExcelUpload
        fields = ('excel_file',)

class ImageForm(forms.ModelForm):
    class Meta:
        model = ReportImages
        fields = ('image', )
ReportImageFormSet = forms.modelformset_factory(ReportImages, form=ImageForm, extra=1)        