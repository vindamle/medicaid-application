# Generated by Django 2.1.4 on 2019-02-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0033_application_application_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='approval_verified',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
