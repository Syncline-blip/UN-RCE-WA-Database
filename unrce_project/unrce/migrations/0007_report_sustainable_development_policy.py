# Generated by Django 4.2.4 on 2023-10-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unrce', '0006_remove_report_address_remove_report_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='sustainable_development_policy',
            field=models.TextField(blank=True, default=''),
        ),
    ]
