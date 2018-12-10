from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('alert_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_priority', models.IntegerField()),
                ('alert_status', models.BooleanField(default=False)),
                ('alert_message', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AlertType',
            fields=[
                ('alert_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationTracking',
            fields=[
                ('tracking_id', models.AutoField(primary_key=True, serialize=False)),
                ('LTC', models.BooleanField(blank=True, null=True)),
                ('spousal', models.BooleanField(blank=True, null=True)),
                ('application_type', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
                ('is_medicaid_pending', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_medicaid_submission', models.DateTimeField(blank=True, null=True)),
                ('medicaid_application', models.FileField(blank=True, null=True, upload_to='applications/')),
                ('medicaid_confirmation', models.FileField(blank=True, null=True, upload_to='applications/')),
                ('date_of_rfi', models.DateTimeField(blank=True, null=True)),
                ('rfi', models.FileField(blank=True, null=True, upload_to='applications/')),
                ('date_of_deadline', models.DateTimeField(blank=True, null=True)),
                ('rfi_deadline_alert', models.BooleanField(blank=True, null=True)),
                ('date_of_medicaid_approval', models.DateTimeField(blank=True, null=True)),
                ('medicaid_approval', models.FileField(blank=True, null=True, upload_to='applications/')),
                ('date_of_medicaid_recertification', models.DateTimeField(blank=True, null=True)),
                ('medicaid_pickup_date', models.DateTimeField(blank=True, null=True)),
                ('approval_start_date', models.DateTimeField(blank=True, null=True)),
                ('approval_end_date', models.DateTimeField(blank=True, null=True)),
                ('approval_notice_date', models.DateTimeField(blank=True, null=True)),
                ('estimated_nami', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('copay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('secondary_pays_copay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('application_state', models.CharField(blank=True, max_length=50, null=True)),
                ('application_county', models.CharField(blank=True, max_length=50, null=True)),
                ('approval_verified', models.BooleanField(blank=True, null=True)),
                ('fair_hearing_required', models.BooleanField(blank=True, null=True)),
                ('fair_hearing_notice_date', models.DateTimeField(blank=True, null=True)),
                ('spousal_refusal', models.BooleanField(blank=True, null=True)),
                ('appointment_required', models.BooleanField(blank=True, null=True)),
                ('appointment_date', models.DateTimeField(blank=True, null=True)),
                ('dss_contact_address', models.CharField(blank=True, max_length=100, null=True)),
                ('dss_contact_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('dss_contact_email', models.EmailField(blank=True, max_length=100, null=True)),
                ('dss_contact_fax', models.CharField(blank=True, max_length=100, null=True)),
                ('notes_file', models.FileField(blank=True, null=True, upload_to='applications/')),
                ('recertification_alert', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'ApplicationTracking',
                'verbose_name_plural': 'ApplicationTracking',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('facility_id', models.AutoField(primary_key=True, serialize=False)),
                ('facility_number', models.IntegerField(blank=True, null=True)),
                ('facility_name', models.CharField(blank=True, max_length=255, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('downstate_upstate', models.CharField(blank=True, max_length=100, null=True)),
                ('centers_grand', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('specialty_rx_facility_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Facilities',
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('resident_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('resident_number', models.IntegerField(blank=True, null=True)),
                ('ssn', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('facility_id', models.IntegerField(blank=True, null=True)),
                ('facility', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_payor_id', models.IntegerField(blank=True, null=True)),
                ('primary_payor_grp', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_payor', models.CharField(blank=True, max_length=50, null=True)),
                ('secondary_payor_id', models.IntegerField(blank=True, null=True)),
                ('secondary_payor_grp', models.CharField(blank=True, max_length=50, null=True)),
                ('secondary_payor', models.CharField(blank=True, max_length=50, null=True)),
                ('activity_date', models.DateTimeField(blank=True, null=True)),
                ('activity_type', models.CharField(blank=True, max_length=2, null=True)),
                ('tracking_status', models.BooleanField(blank=True, null=True)),
                ('sex', models.CharField(blank=True, max_length=2, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('zip', models.IntegerField(blank=True, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Residents',
                'verbose_name_plural': 'Residents',
            },
        ),
        migrations.AddField(
            model_name='applicationtracking',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Resident'),
        ),
        migrations.AddField(
            model_name='alert',
            name='alert_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.AlertType'),
        ),
        migrations.AddField(
            model_name='alert',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.ApplicationTracking'),
        ),
        migrations.AddField(
            model_name='alert',
            name='resident',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Resident'),
        ),
    ]
