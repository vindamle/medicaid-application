# Generated by Django 2.1.4 on 2019-02-06 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0032_alerttype_alert_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
