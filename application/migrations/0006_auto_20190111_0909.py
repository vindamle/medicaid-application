# Generated by Django 2.1.4 on 2019-01-11 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_document_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='application',
        ),
        migrations.AddField(
            model_name='application',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document'),
        ),
        migrations.AddField(
            model_name='document',
            name='Resident',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.Resident'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='application_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
