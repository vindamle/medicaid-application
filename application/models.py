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
    patient_id  = models.AutoField(primary_key=True)
    #ssn = models.CharField(max_length=255, null=True, blank=True)
    fname = models.CharField(max_length=50, null=True, blank=True)
    lname = models.CharField(max_length=50, null=True, blank=True)
    primary_payor = models.CharField(max_length=50, null=True, blank=True)
    secondary_payor = models.CharField(max_length=50, null=True, blank=True)
    activity_date = models.DateTimeField(null=True, blank=True)
    activity_type = models.CharField(max_length=2, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete = models.CASCADE)
    # there will be others
    def __str__(self):
        return self.patient_id

    class Meta:
        verbose_name = 'Alerts'
        verbose_name_plural = 'Alerts'
