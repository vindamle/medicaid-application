# Generated by Django 2.1.4 on 2019-01-11 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_auto_20190111_0909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='Resident',
            new_name='resident',
        ),
    ]