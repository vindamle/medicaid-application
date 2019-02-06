# Generated by Django 2.1.5 on 2019-01-29 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0021_auto_20190129_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='denial',
            name='denial_documentation_submitted_date',
        ),
        migrations.RemoveField(
            model_name='denial',
            name='denial_fair_hearing_request',
        ),
        migrations.RemoveField(
            model_name='denial',
            name='denial_notice_date',
        ),
        migrations.RemoveField(
            model_name='snowden',
            name='row_id',
        ),
        migrations.AddField(
            model_name='snowden',
            name='application',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='application.Application'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snowden',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]