from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django_countries.fields import CountryField

#This model is for the reports 
FREQUENCY_CHOICES = [
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('biannually', 'Biannually'),
    ('annually', 'Annually'),
    ('ongoing', 'Ongoing'),
    ('once', 'Once'),
    ('opportunistic_irregularly', 'Opportunistic/Irregularly'),
    ('permanent_on demand', 'Permanent/On demand'),
]

AUDIENCE_CHOICES = [
    ('general_public', 'General public (any age)'),
    ('particular_audience', 'Particular target Audience (Please specify)'),
    ('primary_school_age', 'Primary School age'),
    ('high_school_age', 'High school age'),
    ('tertiary_students', 'Tertiary students'),
    ('teacher_ed', 'Teacher Ed'),
    ('adults', 'Adults'),
    ('early_years', 'Early years'),
    ('adults_60', 'Adults >60'),
]

DELIVERY_CHOICES = [
    ('hands_on_interactive', 'Hands-on/Interactive'),
    ('presentation_inperson', 'Presentation (in person)'),
    ('presentation_virtual', 'Presentation (virtual)'),
    ('video_resource', 'Video Resource'),
    ('workshop_hackathon', 'Workshop/Hackathon'),
    ('group_meeting', 'Convene and administer group meetings'),
    ('document_toolkit_resource', 'Document/Toolkit/resource'),
    ('experience', 'Experience'),
    ('initiative', 'Initiative'),
    ('community_asset', 'Community Asset'),

]
RCE_CHOICES = [
    ('hands_on_interactive', 'Hands-on/Interactive'),
    ('community_asset', 'Community Asset'),
    ('supported_workplace', 'Supported Workplace Placement'),
    ('document', 'Documemt'),
    ('group_meetings', 'Group Meetings'),

]
ECOSYSTEM_CHOICES = [
    ('agricultural', 'Agricultural'),
    ('coastal', 'Coastal'),
    ('dryland', 'Dryland'),
    ('forest', 'Forest'),
    ('fresh_water', 'Fresh Water'),
    ('grassland', 'Grassland'),
    ('mountain', 'Mountain'),
    ('urban_peri_urban', 'Urban/Peri-urban'),
    ('wetlands', 'Wetlands'),
    ('other', 'Other'),
]
STATUS_CHOICES = [
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('new_report', 'New Report'),
]
REGION_CHOICES = [
    ('test', 'Test'),
    ('demo', 'DEmo'),
]
themes_esd = [
    'Disaster Risk Reduction',
    'Traditional Knowledge',
    'Agriculture',
    'Arts',
    'Curriculum Development',
    'Ecotourism',
    'Forests/Trees',
    'Plants & Animals',
    'Waste'
]

priority_action_areas = [
    'Priority Action Area 1 - Advancing policy',
    'Priority Action Area 2 - Transforming learning and training environments',
    'Priority Action Area 3 - Developing capacities of educators and trainers',
    'Priority Action Area 4 - Mobilizing youth',
    'Priority Action Area 5 - Accelerating sustainable solutions at local level'
]


class Report(models.Model):
#Basic information
    title_project = models.CharField(max_length=200, null=True)
    submitting_RCE = models.CharField(max_length=200, choices=RCE_CHOICES, null=True)

#Focal point(s) and affiliation(s)
    linked_users = models.ManyToManyField(User, related_name='linked_reports', blank=True)
    format_project = models.CharField(max_length=200, null=True)
    delivery = models.CharField(max_length=200, choices=DELIVERY_CHOICES, blank=True, null=True) 
    frequency = models.CharField(max_length=200, choices=FREQUENCY_CHOICES, null=True)
    language_project = models.CharField(max_length=200, null=True)
    web_link = models.URLField(max_length=200, null=True)
    additional_resources = models.TextField(null=True)
    #Sustainable development policy true/false into box

#Geographical & educaiton information
    region = models.CharField(max_length=200, choices=REGION_CHOICES, null=True)
    country = CountryField(null=True)
    locations = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    ecosystem = models.CharField(max_length=200, choices=ECOSYSTEM_CHOICES, null=True)
    audience = ArrayField(
        models.CharField(max_length=200, choices=AUDIENCE_CHOICES),
        blank=True,
        null=True,
    )
    socio_economic_characteristics = models.TextField(null=True)
    development_challenges = models.TextField(null=True)

#Contents
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, null=True)
    start_project = models.DateField(null=True)
    end_project = models.DateField(null=True)
    rationale = models.TextField(null=True)
    objectives = models.TextField(null=True)
    activities_practices = models.TextField(null=True)
    size_academic = models.IntegerField(null=True)
    results = models.TextField(null=True)
    lessons_learned = models.TextField(null=True)
    key_message = models.TextField(null=True)
    relationship_activities = models.TextField(null=True)
    funding = models.TextField(null=True)


#UN Sustainable Development Goals (SDGs)
    direct_sdgs = ArrayField(
        models.IntegerField(),
        blank=True,
        null=True,
    )
    indirect_sdgs = ArrayField(
        models.IntegerField(),
        blank=True,
        null=True,
    )

    direct_esd_themes = ArrayField(
        models.CharField(max_length=255),  # since themes are strings, we store them as CharFields
        blank=True,
        null=True,
    )
    indirect_esd_themes = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
    )

    direct_priority_areas = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
    )
    indirect_priority_areas = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
    )
#Make another set of these for ESD and ESD 2030

    created_at = models.DateField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    approved = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.title_project}   {self.created_at}"



#Model for images to link to reports 
class ReportImages(models.Model):
    report = models.ForeignKey(Report, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

class ReportFiles(models.Model):
    report = models.ForeignKey(Report, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')

class Organization(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.URLField(max_length=200, null=True, blank=True)




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
    def __str__(self):
        return self.user.username

