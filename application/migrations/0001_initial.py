# Generated by Django 2.1.4 on 2019-03-12 16:11

import application.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pgcrypto_expressions.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('alert_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_status', models.BooleanField(default=False)),
                ('trigger_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Alerts',
                'verbose_name_plural': 'Alerts',
            },
        ),
        migrations.CreateModel(
            name='AlertType',
            fields=[
                ('alert_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_name', models.CharField(max_length=50)),
                ('alert_priority', models.IntegerField()),
                ('alert_class', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateTimeField(blank=True, null=True)),
                ('medicaid_eligible', models.CharField(blank=True, max_length=50, null=True)),
                ('ltc', models.CharField(blank=True, max_length=50, null=True)),
                ('spousal', models.CharField(blank=True, max_length=50, null=True)),
                ('application_type', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_application_submission', models.DateTimeField(blank=True, null=True)),
                ('date_of_application_submission_deadline', models.DateTimeField(blank=True, null=True)),
                ('medicaid_pickup_date', models.DateField(blank=True, null=True)),
                ('estimated_nami', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('copay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('copay_start_date', models.DateTimeField(blank=True, null=True)),
                ('secondary_pays_copay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('application_state', models.CharField(blank=True, max_length=50, null=True)),
                ('application_county', models.CharField(blank=True, max_length=50, null=True)),
                ('spousal_refusal', models.CharField(blank=True, max_length=50, null=True)),
                ('initial_response', models.CharField(blank=True, max_length=20, null=True)),
                ('dss_contact_address', models.CharField(blank=True, max_length=100, null=True)),
                ('dss_contact_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('dss_contact_email', models.EmailField(blank=True, max_length=100, null=True)),
                ('dss_contact_fax', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_status', models.BooleanField(blank=True, null=True)),
                ('application_creation_date', models.DateField(auto_now_add=True)),
                ('approval_verified', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Applications',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('approval_id', models.AutoField(primary_key=True, serialize=False)),
                ('approval_start_date', models.DateTimeField(blank=True, null=True)),
                ('approval_end_date', models.DateTimeField(blank=True, null=True)),
                ('approval_recertification_date', models.DateTimeField(blank=True, null=True)),
                ('approval_notice_date', models.DateTimeField(blank=True, null=True)),
                ('approval_satisfied', models.CharField(blank=True, max_length=50, null=True)),
                ('approval_contacted_dss', models.CharField(blank=True, max_length=50, null=True)),
                ('approval_resolved_through_dss', models.CharField(blank=True, max_length=50, null=True)),
                ('approval_fair_hearing_required', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Approvals',
                'verbose_name_plural': 'Approvals',
            },
        ),
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('confirmation_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('date_uploaded', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Confirmations',
                'verbose_name_plural': 'Confirmations',
            },
        ),
        migrations.CreateModel(
            name='Denial',
            fields=[
                ('denial_id', models.AutoField(primary_key=True, serialize=False)),
                ('denial_notice_date', models.DateTimeField(blank=True, null=True)),
                ('denial_fair_hearing_requested', models.CharField(blank=True, max_length=50, null=True)),
                ('denial_documentation_submitted', models.CharField(blank=True, max_length=50, null=True)),
                ('denial_contacted_dss', models.CharField(blank=True, max_length=50, null=True)),
                ('denial_resolved_through_dss', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Denials',
                'verbose_name_plural': 'Denials',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('application_id', models.IntegerField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=application.models.get_path)),
                ('file_name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('date_uploaded', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Documents',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('Boro Park', 'Boro Park'), ('Brooklyn', 'Brooklyn'), ('Bushwick', 'Bushwick'), ('Washington', 'Washington'), ('Corning', 'Corning'), ('Argyle Center', 'Argyle Center'), ('Bronx', 'Bronx'), ('Warren', 'Warren'), ('Deptford', 'Deptford'), ('Oak Hill', 'Oak Hill'), ('Beth Abraham', 'Bet Abraham'), ('Essex', 'Essex'), ('Far Rockaway', 'Far Rockaway'), ('Fulton', 'Fulton'), ('Carthage', 'Carthage'), ('Hammonton', 'Hammonton'), ('Holliswood', 'Holliswood'), ('Hope Center', 'Hope Center'), ('WC - Elm Manor', 'WC - Elm Manor'), ('Mount Laurel', 'Mount Laurel'), ('N. Manor', 'Northern Manor'), ('Ellicott', 'Ellicott Center'), ('N. Metropolitan', 'N. Metropolitan'), ('Glens Falls', 'Glens Falls'), ('N. Riverview', 'N. Riverview'), ('New Paltz', 'New Paltz'), ('Ontario Center', 'Ontario Center'), ('Ontario County', 'Ontario County'), ('STBN County', 'STBN County'), ('Onondaga', 'Onondaga'), ('PG - Quality Care', 'Quality Care'), ('PG - Stamford Residence', 'Stamford Residence'), ('PG - Walnut Hills', 'Walnut Hills'), ('PG - Westview Manor', 'Westview Manor'), ('Claremont ALP', 'Claremont'), ('Steuben', 'Steuben'), ('Suffolk', 'Suffolk'), ('University', 'University'), ('Williamsbridge', 'Williamsbridge'), ('Bannister', 'Bannister'), ('Buffalo', 'Buffalo'), ('Park View', 'Park View'), ('Schenectady', 'Schenectady'), ('Slate Valley', 'Slate Valley'), ('Triboro (ALP)', 'Alpine Triboro Center'), ('Triboro Center', 'Triboro Center'), ('Troy', 'Troy'), ('Centers for Care', 'Centers for Care'), ('Brookside - MA', 'Brookside'), ('Granville', 'Granville'), ('Evolve', 'Evolve'), ('Kingston', 'Kingston'), ('New Boston', 'New Boston'), ('WC - Wedgewood', 'Wedgewood'), ('Cooperstown', 'Cooperstown'), ('Martine', 'Martine'), ('Focus - Otsego - Charts', 'Otsego'), ('Focus - Utica - Charts', 'Utica'), ('EC - Midwest', 'Midwest'), ('EC - Southwest', 'Southwest Center'), ('Mills Pond', 'Mills Pond'), ('Sayville', 'Sayville'), ('Birchwood - VT', 'Birchwood'), ('WC - Folts ADC', 'Folts ADC'), ('EC - Tulsa', 'Tulsa'), ('EC - Claremore', 'Claremore'), ('EC - Memory Care', 'Memory Care'), ('Castle Senior Living', 'Castle Senior Living'), ('Focus Senior Living', 'Focus Senior Living'), ('Richmond (Staten Island)', 'Richmond Center'), ('WC - Folts Home', 'Folts Home'), ('Creekview', 'Creekview'), ('EC - Crystal', 'Crystal Center'), ('EC - Pikeville', 'Pikeville'), ('Kansas City ALF', 'Kansas City ALF'), ('Overland Park ALF', 'Overland Park ALF'), ('Oneida Center', 'Oneida Center'), ('Butler Center', 'Butler Center'), ('Kansas City', 'Kansas City'), ('Overland Park', 'Overland Park'), ('Ten Broeck', 'Ten Broeck'), ('Topeka Center', 'Topeka Center'), ('Wichita Center', 'Wichita Center')),
                'verbose_name': 'Employees',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('facility_id', models.AutoField(primary_key=True, serialize=False)),
                ('facility_pcc_id', models.IntegerField(blank=True, null=True)),
                ('facility_name', models.CharField(blank=True, max_length=100, null=True)),
                ('facility_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'Facilities',
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='FairHearing',
            fields=[
                ('fair_hearing_id', models.AutoField(primary_key=True, serialize=False)),
                ('fair_hearing_date', models.DateField(blank=True, null=True)),
                ('fair_hearing_time', models.TimeField(blank=True, null=True)),
                ('fair_hearing_address', models.CharField(blank=True, max_length=50, null=True)),
                ('fair_hearing_outcome', models.CharField(blank=True, max_length=50, null=True)),
                ('fair_hearing_representative_type', models.CharField(blank=True, max_length=50, null=True)),
                ('fair_hearing_representative_name', models.CharField(blank=True, max_length=100, null=True)),
                ('fair_hearing_satisfied', models.CharField(blank=True, max_length=10, null=True)),
                ('fair_hearing_outcome_date', models.DateField(blank=True, null=True)),
                ('fair_hearing_confirmation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Confirmation')),
                ('fair_hearing_outcome_document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document')),
            ],
            options={
                'verbose_name': 'Fair Hearings',
                'verbose_name_plural': 'Fair Hearings',
            },
        ),
        migrations.CreateModel(
            name='NAMI',
            fields=[
                ('nami_id', models.AutoField(primary_key=True, serialize=False)),
                ('nami_start_date', models.DateField(blank=True, null=True)),
                ('nami_end_date', models.DateField(blank=True, null=True)),
                ('nami_amount', models.FloatField(blank=True, null=True)),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Approval')),
            ],
            options={
                'verbose_name': 'NAMIS',
                'verbose_name_plural': 'NAMIS',
            },
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('phase_id', models.AutoField(primary_key=True, serialize=False)),
                ('phase_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Phases',
                'verbose_name_plural': 'Phases',
            },
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('resident_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('resident_number', models.IntegerField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('ssn', pgcrypto_expressions.fields.EncryptedCharField(blank=True, max_length=50, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('sex', models.CharField(blank=True, max_length=2, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('county', models.CharField(blank=True, max_length=50, null=True)),
                ('zip', models.IntegerField(blank=True, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('facility_id', models.IntegerField(blank=True, null=True)),
                ('facility_name', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_payor_id', models.IntegerField(blank=True, null=True)),
                ('primary_payor_grp', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_payor', models.CharField(blank=True, max_length=50, null=True)),
                ('secondary_payor_id', models.IntegerField(blank=True, null=True)),
                ('secondary_payor_grp', models.CharField(blank=True, max_length=50, null=True)),
                ('secondary_payor', models.CharField(blank=True, max_length=50, null=True)),
                ('activity_date', models.DateTimeField(blank=True, null=True)),
                ('activity_type', models.CharField(blank=True, max_length=2, null=True)),
                ('tracking_status', models.BooleanField(blank=True, null=True)),
                ('dismiss', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Residents',
                'verbose_name_plural': 'Residents',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('response_id', models.AutoField(primary_key=True, serialize=False)),
                ('response_date', models.DateField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Application')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document')),
            ],
            options={
                'verbose_name': 'Responses',
                'verbose_name_plural': 'Responses',
            },
        ),
        migrations.CreateModel(
            name='ResponseType',
            fields=[
                ('response_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('response_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Response Types',
                'verbose_name_plural': 'Response Types',
            },
        ),
        migrations.CreateModel(
            name='RFI',
            fields=[
                ('rfi_id', models.AutoField(primary_key=True, serialize=False)),
                ('rfi_due_date', models.DateTimeField(blank=True, null=True)),
                ('rfi_extension_request', models.CharField(blank=True, max_length=50, null=True)),
                ('rfi_extension_response', models.CharField(blank=True, max_length=50, null=True)),
                ('rfi_documentation_submitted', models.CharField(blank=True, max_length=50, null=True)),
                ('rfi_documentation_submitted_date', models.DateField(blank=True, null=True)),
                ('rfi_response', models.CharField(blank=True, max_length=20, null=True)),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Response')),
            ],
            options={
                'verbose_name': 'RFIS',
                'verbose_name_plural': 'RFIS',
            },
        ),
        migrations.CreateModel(
            name='Snowden',
            fields=[
                ('log_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('row_id', models.IntegerField()),
                ('table_name', models.CharField(max_length=50)),
                ('column_name', models.CharField(max_length=50)),
                ('old_value', models.CharField(max_length=250)),
                ('new_value', models.CharField(max_length=250)),
                ('log_ip', models.GenericIPAddressField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Edward Snowden',
                'verbose_name_plural': 'Edward Snowden',
            },
        ),
        migrations.AddField(
            model_name='response',
            name='response_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.ResponseType'),
        ),
        migrations.AddField(
            model_name='fairhearing',
            name='response',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Response'),
        ),
        migrations.AddField(
            model_name='document',
            name='resident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Resident'),
        ),
        migrations.AddField(
            model_name='denial',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document'),
        ),
        migrations.AddField(
            model_name='denial',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Response'),
        ),
        migrations.AddField(
            model_name='confirmation',
            name='confirmation_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Document'),
        ),
        migrations.AddField(
            model_name='approval',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document'),
        ),
        migrations.AddField(
            model_name='approval',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Response'),
        ),
        migrations.AddField(
            model_name='application',
            name='application_confirmation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Confirmation'),
        ),
        migrations.AddField(
            model_name='application',
            name='application_document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Document'),
        ),
        migrations.AddField(
            model_name='application',
            name='phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Phase'),
        ),
        migrations.AddField(
            model_name='application',
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
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Application'),
        ),
        migrations.AddField(
            model_name='alert',
            name='resident',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Resident'),
        ),
    ]
