# Generated by Django 4.2.4 on 2023-10-14 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unrce', '0003_account_requesting'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
