# Generated by Django 2.1.2 on 2019-01-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20190109_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationtracking',
            name='date_of_medicaid_submission',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
