# Generated by Django 4.2.4 on 2023-09-19 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unrce', '0021_alter_report_audience_alter_report_delivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='project_description_long',
            field=models.CharField(max_length=3000, null=True),
        ),
    ]