# Generated by Django 2.1.4 on 2019-01-24 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_auto_20190124_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snowden',
            name='log_ip',
            field=models.GenericIPAddressField(),
        ),
    ]