# Generated by Django 2.1.4 on 2019-01-11 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20190111_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='document',
            new_name='application_document',
        ),
    ]