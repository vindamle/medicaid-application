# Generated by Django 2.1 on 2018-10-26 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_auto_20181026_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('ssn', models.CharField(blank=True, max_length=255, null=True)),
                ('fisrt_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_payor', models.CharField(blank=True, max_length=50, null=True)),
                ('secondary_payor', models.CharField(blank=True, max_length=50, null=True)),
                ('activity_date', models.DateTimeField(blank=True, null=True)),
                ('activity_type', models.CharField(blank=True, max_length=2, null=True)),
                ('tracking_status', models.BooleanField(blank=True, null=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Facility')),
            ],
            options={
                'verbose_name': 'Alerts',
                'verbose_name_plural': 'Alerts',
            },
        ),
    ]
