# Generated by Django 2.1.4 on 2019-01-24 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_auto_20190124_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'permissions': (('Beth Abraham', 'Can View Beth Abraham Center Residents'), ('Boro Park', 'Can View Boro Park Center Residents'), ('Steuben', 'Can View Boro Park Center Residents'))},
        ),
    ]
