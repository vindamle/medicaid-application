# Generated by Django 2.1.4 on 2019-04-02 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_denial_denial_letter_received'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='denial',
            name='denial_letter_received',
        ),
        migrations.AddField(
            model_name='denial',
            name='no_denial_letter_received',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
