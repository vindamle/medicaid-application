# Generated by Django 2.1 on 2018-11-12 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20181107_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackingdata',
            name='recertification_alert',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trackingdata',
            name='rfi_deadline_alert',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
