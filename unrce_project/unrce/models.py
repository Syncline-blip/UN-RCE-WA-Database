from django.db import models

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