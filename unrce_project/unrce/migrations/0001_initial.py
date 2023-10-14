# Generated by Django 4.2.4 on 2023-10-14 05:32

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_project', models.CharField(default='', max_length=200)),
                ('delivery', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('hands_on_interactive', 'Hands-on/Interactive'), ('presentation_inperson', 'Presentation (in person)'), ('presentation_virtual', 'Presentation (virtual)'), ('video_resource', 'Video Resource'), ('workshop_hackathon', 'Workshop/Hackathon'), ('group_meeting', 'Convene and administer group meetings'), ('document_toolkit_resource', 'Document/Toolkit/resource'), ('experience', 'Experience'), ('initiative', 'Initiative'), ('community_asset', 'Community Asset')], max_length=200), blank=True, default=list, null=True, size=None)),
                ('frequency', models.CharField(choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('biannually', 'Biannually'), ('annually', 'Annually'), ('ongoing', 'Ongoing'), ('once', 'Once'), ('opportunistic_irregularly', 'Opportunistic/Irregularly'), ('permanent_on demand', 'Permanent/On demand')], max_length=200, null=True)),
                ('web_link', models.URLField(blank=True, default='')),
                ('additional_resources', models.TextField(blank=True, default='')),
                ('region', models.CharField(choices=[('perth_metro', 'Perth Metro'), ('great_southern', 'Great Southern'), ('wa', 'WA')], max_length=200, null=True)),
                ('ecosystem', models.CharField(blank=True, choices=[('agricultural', 'Agricultural'), ('coastal', 'Coastal'), ('dryland', 'Dryland'), ('forest', 'Forest'), ('fresh_water', 'Fresh Water'), ('grassland', 'Grassland'), ('mountain', 'Mountain'), ('urban_peri_urban', 'Urban/Peri-urban'), ('wetlands', 'Wetlands'), ('other', 'Other')], default='', max_length=200)),
                ('audience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('general_public', 'General public (any age)'), ('particular_audience', 'Particular target Audience (Please specify)'), ('primary_school_age', 'Primary School age'), ('high_school_age', 'High school age'), ('tertiary_students', 'Tertiary students'), ('teacher_ed', 'Teacher Ed'), ('adults', 'Adults'), ('early_years', 'Early years'), ('adults_60', 'Adults >60')], max_length=200), blank=True, default=list, null=True, size=None)),
                ('socio_economic_characteristics', models.TextField(blank=True, default='')),
                ('development_challenges', models.TextField(blank=True, default='')),
                ('sustainable_development_policy', models.TextField(blank=True, default='')),
                ('status', models.CharField(blank=True, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('new_report', 'New Report')], max_length=200, null=True)),
                ('start_project', models.DateField(blank=True, null=True)),
                ('end_project', models.DateField(blank=True, null=True)),
                ('rationale', models.TextField(blank=True, default='')),
                ('objectives', models.TextField(blank=True, default='')),
                ('activities_practices', models.TextField(blank=True, default='')),
                ('size_academic', models.IntegerField(blank=True, default=None, null=True)),
                ('results', models.TextField(blank=True, default='')),
                ('lessons_learned', models.TextField(blank=True, default='')),
                ('key_message', models.TextField(blank=True, default='')),
                ('relationship_activities', models.TextField(blank=True, default='')),
                ('funding', models.TextField(blank=True, default='')),
                ('direct_sdgs', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('indirect_sdgs', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('direct_esd_themes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None)),
                ('indirect_esd_themes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None)),
                ('direct_priority_areas', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None)),
                ('indirect_priority_areas', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
                ('submitted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReportImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='unrce.report')),
            ],
        ),
        migrations.CreateModel(
            name='ReportFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='unrce.report')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('website', models.URLField(blank=True, default='', null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unrce.report')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=100)),
                ('profile_sdg', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None)),
                ('sector', models.CharField(choices=[('mining', 'Mining'), ('retail', 'Retail'), ('finance', 'Finance'), ('construction', 'Construction'), ('trade', 'Trade'), ('transport', 'Transport'), ('agriculture', 'Agriculture'), ('education', 'Education'), ('investment', 'Investment'), ('health_care', 'Health Care'), ('small_business', 'Small Business'), ('postal_and_warehousing', 'Postal and Warehousing'), ('management', 'Management'), ('computers_and_information_technology', 'Computers and Information Technology'), ('law', 'Law'), ('financial_services', 'Financial Services'), ('bank', 'Bank'), ('energy_industry', 'Energy Industry'), ('coal', 'Coal'), ('management_consulting', 'Management Consulting'), ('food_industry', 'Food Industry'), ('agribusiness', 'Agribusiness'), ('infrastructure', 'Infrastructure'), ('engineering', 'Engineering'), ('hospitality_industry', 'Hospitality Industry'), ('commercial_bank', 'Commercial Bank'), ('international_trade', 'International Trade'), ('e_commerce', 'E-Commerce'), ('natural_resource', 'Natural Resource'), ('telecommunications', 'Telecommunications'), ('startup_company', 'Startup Company'), ('electronic_business', 'Electronic Business'), ('hospitality', 'Hospitality'), ('accounting', 'Accounting'), ('entertainment', 'Entertainment'), ('aviation', 'Aviation')], max_length=200, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
