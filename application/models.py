from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)


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

class Alert(models.Model):
    patient_id  = models.BigAutoField(primary_key=True)
    patient_number = models.IntegerField(null = True, blank = True)
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
    # there will be others
    def __str__(self):
        return self.patient_id

    class Meta:
        verbose_name = 'Alerts'
        verbose_name_plural = 'Alerts'


class TrackingData(models.Model):
    patient = models.OneToOneField(
        Alert,
        on_delete = models.CASCADE,
        primary_key=True
    )
    show_errors  = models.BooleanField(null = True, blank = True)
    address = models.CharField(max_length = 100, null = True, blank = True)
    city = models.CharField(max_length = 50, null = True, blank = True)
    state = models.CharField(max_length = 50, null = True, blank = True)
    zip = models.IntegerField(null = True, blank = True)
    status = models.BooleanField(null = True, blank = True)
    is_medicaid_pending =  models.CharField(max_length = 50, null = True, blank = True)
    medicaid_pickup_date = models.DateTimeField(null = True, blank = True)

    application_type = models.CharField(max_length = 5, null = True, blank = True)
    date_of_medicaid_submission  = models.DateTimeField(null = True, blank = True)
    medicaid_application = models.FileField(upload_to = 'applications/',null = True, blank = True)
    medicaid_comfirmation = models.FileField(upload_to = 'applications/',null = True, blank = True)

    date_of_rfi  = models.DateTimeField(null = True, blank = True)
    rfi = models.FileField(upload_to = 'applications/',null = True, blank = True)
    date_of_deadline  = models.DateTimeField(null = True, blank = True)

    date_of_medicaid_approval  = models.DateTimeField(null = True, blank = True)
    medicaid_approval = models.FileField(upload_to = 'applications/',null = True, blank = True)
    date_of_medicaid_recertification  = models.DateTimeField(null = True, blank = True)


    # there will be others
    def __str__(self):
        return self.patient_id

    class Meta:
        verbose_name = 'TrackingData'
        verbose_name_plural = 'TrackingData'
