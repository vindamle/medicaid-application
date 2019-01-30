# Generated by Django 2.1.4 on 2019-01-30 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0023_auto_20190129_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approval',
            old_name='fair_hearing_required',
            new_name='approval_contacted_dss',
        ),
        migrations.RenameField(
            model_name='approval',
            old_name='satisfied_with_approval',
            new_name='approval_fair_hearing_required',
        ),
        migrations.RenameField(
            model_name='denial',
            old_name='document',
            new_name='denial_document',
        ),
        migrations.RemoveField(
            model_name='fairhearing',
            name='fair_hearing_appeal',
        ),
        migrations.AddField(
            model_name='approval',
            name='approval_resolved_through_dss',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='approval',
            name='approval_satisfied',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='denial',
            name='denial_contacted_dss',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='denial',
            name='denial_documentation_submitted',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='denial',
            name='denial_fair_hearing_requested',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='denial',
            name='denial_notice_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='denial',
            name='denial_resolved_through_dss',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]