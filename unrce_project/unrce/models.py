from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

#This model is for the reports 
FREQUENCY_CHOICES = [
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('annually', 'Annually'),
    ('biannually', 'Biannually'),
    ('quarterly', 'Quarterly'),
    ('seasonally', 'Seasonally'),
    ('as_required', 'As Required'),
    ('custom', 'Custom'),
]

AUDIENCE_CHOICES = [
    ('community', 'Community'),
    ('primary_students', 'Primary School Students'),
    ('secondary_students', 'Secondary School Students'),
    ('higher_education', 'Higher Education'),
    ('teacher_ed', 'Teacher Ed'),
    ('youth_informal', 'Youth(informal)'),
    ('youth_formal', 'Youth(formal)'),
    ('professionals', 'Professionals'),
    ('public_anyage', 'General Public (any age)'),
    ('public_older', 'General Public (>60)'),
    ('public_adults', 'General Public (adults)'),
    ('public_younger', 'General Public (< 20)'),
    ('buisness_government', 'Buisness and Government'),
]

DELIVERY_CHOICES = [
    ('hands_on_interactive', 'Hands-on/Interactive'),
    ('community_asset', 'Community Asset'),
    ('supported_workplace', 'Supported Workplace Placement'),
    ('document', 'Documemt'),
    ('group_meetings', 'Group Meetings'),

]

class Report(models.Model):
    lead_organisation = models.CharField(max_length=200)
    name_project = models.CharField(max_length=200)
    project_description_short = models.CharField(max_length=200)
    project_description_long = models.CharField(max_length=5000 , null=True)
    delivery = ArrayField(
        models.CharField(max_length=20, choices=DELIVERY_CHOICES),
        blank=True,
        null=True,
    )
    frequency = models.CharField(max_length=200, choices=FREQUENCY_CHOICES)
    audience = ArrayField(
        models.CharField(max_length=20, choices=AUDIENCE_CHOICES),
        blank=True,
        null=True,
    )
    current_partners = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    sdg_focus = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name_project}   {self.created_at}"

#Model for images to link to reports 
class ReportImages(models.Model):
    report = models.ForeignKey(Report, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    
#Model for uploading excel documents 
class ExcelUpload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    excel_file = models.FileField(upload_to='excels/')

#Model for the expression of interest, in UNRCE
class Expression_of_interest(models.Model):
    title_of_project = models.CharField(max_length=200)
    contributing_organizations = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    organisation_affiliation = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, default='default@email.com')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title_of_project}  {self.created_at}"

# Account Model
class Account(models.Model):
    ''' 
        OneToOneField: Foreign Key 1:1 relationship between Account and User model
        use CASCADE to delete both account and user object
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_name = models.CharField(max_length=30)
    def __str__(self):
        return self.user.username
    