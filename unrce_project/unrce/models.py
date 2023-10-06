from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

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
    ('perth_metro', 'Perth Metro'),
    ('great_southern', 'Great Southern'),
    ('wa', 'WA'),
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
    title_project = models.CharField(max_length=200, default='')

    # Focal point(s) and affiliation(s)
    delivery = ArrayField(
        models.CharField(max_length=200, choices=DELIVERY_CHOICES),
        blank=True,
        null=True,
        default=list
    )
    frequency = models.CharField(max_length=200, choices=FREQUENCY_CHOICES, null=True)
    web_link = models.URLField(max_length=200, blank=True, default='')
    additional_resources = models.TextField(blank=True, default='')

    # Geographical & education information
    region = models.CharField(max_length=200, choices=REGION_CHOICES, null=True)
    ecosystem = models.CharField(max_length=200, choices=ECOSYSTEM_CHOICES, blank=True, default='')
    audience = ArrayField(
        models.CharField(max_length=200, choices=AUDIENCE_CHOICES),
        blank=True,
        null=True,
        default=list
    )
    socio_economic_characteristics = models.TextField(blank=True, default='')
    development_challenges = models.TextField(blank=True, default='')
    sustainable_development_policy = models.TextField(blank=True, default='')

    # Contents
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, null=True, blank=True)
    start_project = models.DateField(blank=True, null=True) 
    end_project = models.DateField(blank=True, null=True)    
    rationale = models.TextField(blank=True, default='')
    objectives = models.TextField(blank=True, default='')
    activities_practices = models.TextField(blank=True, default='')
    size_academic = models.IntegerField(blank=True, null=True, default=None)
    results = models.TextField(blank=True, default='')
    lessons_learned = models.TextField(blank=True, default='')
    key_message = models.TextField(blank=True, default='')
    relationship_activities = models.TextField(blank=True, default='')
    funding = models.TextField(blank=True, default='')



#UN Sustainable Development Goals (SDGs)
    direct_sdgs = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
    )
    indirect_sdgs = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
    )

    direct_esd_themes = ArrayField(
        models.CharField(max_length=255), 
        blank=True,
        default=list
    )
    indirect_esd_themes = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list
    )

    direct_priority_areas = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list
    )
    indirect_priority_areas = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list
    )

    # Additional fields
    created_at = models.DateField(auto_now_add=True) 
    last_modified = models.DateTimeField(auto_now=True)  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    approved = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)

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
    name = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True, default='')




#Model for the expression of interest, in UNRCE
class Expression_of_interest(models.Model):
    title_of_project = models.CharField(max_length=200)
    contributing_organizations = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    organisation_affiliation = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, default='default@email.com')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

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

