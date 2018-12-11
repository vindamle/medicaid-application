from django.db import models
# from django.contrib.auth.models import User

# Create your models here.

# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.CharField(max_length=100)
#

class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_number= models.IntegerField(null=True, blank=True)
    facility_name = models.CharField(max_length=255, null=True, blank=True)
    capacity =  models.IntegerField(null=True, blank=True)
    downstate_upstate= models.CharField(max_length=100, null=True, blank=True)
    centers_grand = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    specialty_rx_facility_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.facility_name

    class Meta:
        verbose_name = 'Facilities'
        verbose_name_plural = 'Facilities'

class Resident(models.Model):

    resident_id  = models.BigAutoField(primary_key=True)
    resident_number = models.IntegerField(null = True, blank = True)
    ssn = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    facility_id = models.IntegerField(null = True, blank = True)
    facility = models.CharField(max_length=50, null=True, blank=True)
    primary_payor_id = models.IntegerField(null = True, blank = True)
    primary_payor_grp = models.CharField(max_length=50, null=True, blank=True)
    primary_payor = models.CharField(max_length=50, null=True, blank=True)
    secondary_payor_id =  models.IntegerField(null = True, blank = True)
    secondary_payor_grp = models.CharField(max_length=50, null=True, blank=True)
    secondary_payor = models.CharField(max_length=50, null=True, blank=True)
    activity_date = models.DateTimeField(null=True, blank=True)
    activity_type = models.CharField(max_length=2, null=True, blank=True)
    tracking_status = models.BooleanField(null = True, blank = True)
    sex= models.CharField(max_length=2, null=True, blank=True)
    # first_name_num = models.IntegerField(null = True, blank = True)
    # last_name_num = models.IntegerField(null = True, blank = True)

    address = models.CharField(max_length = 100, null = True, blank = True)
    city = models.CharField(max_length = 50, null = True, blank = True)
    state = models.CharField(max_length = 50, null = True, blank = True)
    county = models.CharField(max_length = 50, null = True, blank = True)
    zip = models.IntegerField(null = True, blank = True)
    marital_status = models.CharField(max_length = 50, null = True, blank = True)


    # there will be others
    def __str__(self):
        return self.resident_id

    class Meta:
        verbose_name = 'Residents'
        verbose_name_plural = 'Residents'


class ApplicationTracking(models.Model):
    tracking_id = models.AutoField(primary_key = True)
    resident = models.ForeignKey(
        Resident,
        on_delete = models.CASCADE,
    )
    LTC = models.BooleanField(max_length = 50,null = True, blank = True)

    spousal = models.CharField (max_length = 50,null = True, blank = True)
    application_type = models.CharField(max_length = 50, null = True, blank = True)


    status = models.BooleanField(null = True, blank = True)
    is_medicaid_pending =  models.CharField(max_length = 50, null = True, blank = True)

    date_of_medicaid_submission  = models.DateTimeField(null = True, blank = True)
    medicaid_application = models.FileField(upload_to = 'applications/',null = True, blank = True)
    medicaid_comfirmation = models.FileField(upload_to = 'applications/',null = True, blank = True)

    date_of_rfi  = models.DateTimeField(null = True, blank = True)
    rfi = models.FileField(upload_to = 'applications/',null = True, blank = True)
    date_of_deadline  = models.DateTimeField(null = True, blank = True)

    date_of_medicaid_approval  = models.DateTimeField(null = True, blank = True)
    medicaid_approval = models.FileField(upload_to = 'applications/',null = True, blank = True)
    date_of_medicaid_recertification  = models.DateTimeField(null = True, blank = True)

    medicaid_pickup_date = models.DateTimeField(null = True, blank = True)
    approval_start_date = models.DateTimeField(null = True, blank = True)
    approval_end_date = models.DateTimeField(null = True, blank = True)
    approval_notice_date = models.DateTimeField(null = True, blank = True)
    estimated_nami = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank = True)
    copay  = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank = True)
    secondary_pays_copay  = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank = True)
    application_state = models.CharField(max_length = 50, null = True, blank = True)
    application_county = models.CharField(max_length = 50, null = True, blank = True)
    approval_verified  = models.BooleanField(null = True, blank = True)
    fair_hearing_required  = models.BooleanField(null = True, blank = True)
    fair_hearing_notice_date = models.DateTimeField(null = True, blank = True)
    spousal_refusal  = models.BooleanField(null = True, blank = True)

    appointment_date = models.DateTimeField(null = True, blank = True)
    dss_contact_address  = models.CharField(max_length = 100, null = True, blank = True)
    dss_contact_phone  = models.CharField(max_length = 100, null = True, blank = True)
    dss_contact_email = models.EmailField(max_length = 100, null = True, blank = True)
    dss_contact_fax  = models.CharField(max_length = 100, null = True, blank = True)
    notes_file = models.FileField(upload_to = 'applications/',null = True, blank = True)



    class Meta:
        verbose_name = 'ApplicationTracking'
        verbose_name_plural = 'ApplicationTracking'

class AlertType(models.Model):

    alert_type_id = models.AutoField(primary_key = True)
    alert_name = models.CharField(max_length = 20,  null = False, blank=False)

class Alert(models.Model):
    alert_id = models.AutoField(primary_key = True)
    resident = models.ForeignKey(
        Resident,
        on_delete = models.CASCADE,
        null = True,
    )
    application = models.ForeignKey(
        ApplicationTracking,
        on_delete = models.CASCADE,
        null = True,
    )
    alert_type = models.ForeignKey(
        AlertType,
        on_delete = models.CASCADE,
    )

    alert_priority = models.IntegerField(null=False,blank=False)
    alert_status =models.BooleanField(default = False)
    alert_message =models.CharField(max_length = 100,  null = False, blank=False)
