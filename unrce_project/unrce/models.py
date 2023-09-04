from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    lead_organisation = models.CharField(max_length=200)
    name_project = models.CharField(max_length=200)
    project_description = models.CharField(max_length=200)
    delivery = models.CharField(max_length=200)
    frequency = models.CharField(max_length=200)
    audience = models.CharField(max_length=200)
    current_partners = models.CharField(max_length=200)
    sdg_focus = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name_project}   {self.created_at}"

class Expression_of_interest(models.Model):
    title_of_project = models.CharField(max_length=200)
    submitting_rce = models.CharField(max_length=200)
    contributing_organizations = models.CharField(max_length=200)
    format = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    web_link = models.CharField(max_length=200)
    additional_resources = models.CharField(max_length=200)
    policy = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    ecosystem = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    socio = models.CharField(max_length=200)
    challenges = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    period = models.CharField(max_length=200)
    rationale = models.CharField(max_length=200)
    objectives = models.CharField(max_length=200)
    activites = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    results = models.CharField(max_length=200)
    lessons = models.CharField(max_length=200)
    key_msg = models.CharField(max_length=200)
    relationships = models.CharField(max_length=200)
    funding = models.CharField(max_length=200)
    pictures = models.CharField(max_length=200)
    sdg = models.CharField(max_length=200)
    priority = models.CharField(max_length=200)

