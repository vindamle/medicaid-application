from django.db import models
from pathlib import Path
# from django.contrib.auth.models import User

# Create your models here.

# class Facility(models.Model):
#     facility_id = models.AutoField(primary_key=True)
#     facility_number= models.IntegerField(null=True, blank=True)
#     facility_name = models.CharField(max_length=255, null=True, blank=True)
#     capacity =  models.IntegerField(null=True, blank=True)
#     downstate_upstate= models.CharField(max_length=100, null=True, blank=True)
#     centers_grand = models.CharField(max_length=100, null=True, blank=True)
#     start_date = models.DateTimeField(null=True, blank=True)
#     specialty_rx_facility_name = models.CharField(max_length=255, null=True, blank=True)
#
#     def __str__(self):
#         return self.facility_name
#
#     class Meta:
#         verbose_name = 'Facilities'
#         verbose_name_plural = 'Facilities'

class Resident(models.Model):
    resident_id  = models.BigAutoField(primary_key=True)
    resident_number = models.IntegerField(null = True, blank = True)

    #Patient Info
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    ssn = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    sex= models.CharField(max_length=2, null=True, blank=True)
    address = models.CharField(max_length = 100, null = True, blank = True)
    city = models.CharField(max_length = 50, null = True, blank = True)
    state = models.CharField(max_length = 50, null = True, blank = True)
    county = models.CharField(max_length = 50, null = True, blank = True)
    zip = models.IntegerField(null = True, blank = True)
    marital_status = models.CharField(max_length = 50, null = True, blank = True)
    phone = models.CharField(max_length = 50, null = True, blank = True)

    #Facility Info
    facility_id = models.IntegerField(null = True, blank = True)
    facility_name = models.CharField(max_length=50, null=True, blank=True)

    # Primary Payor Info
    primary_payor_id = models.IntegerField(null = True, blank = True)
    primary_payor_grp = models.CharField(max_length=50, null=True, blank=True)
    primary_payor = models.CharField(max_length=50, null=True, blank=True)

    # Secondary Payor Info
    secondary_payor_id =  models.IntegerField(null = True, blank = True)
    secondary_payor_grp = models.CharField(max_length=50, null=True, blank=True)
    secondary_payor = models.CharField(max_length=50, null=True, blank=True)

    # Activity Info
    activity_date = models.DateTimeField(null=True, blank=True)
    activity_type = models.CharField(max_length=2, null=True, blank=True)

    # Tracking Info
    tracking_status = models.BooleanField(null = True, blank = True)
    dismiss = models.BooleanField(default = False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Residents'
        verbose_name_plural = 'Residents'

class Phase(models.Model):
    phase_id = models.AutoField(primary_key = True)
    phase_name = models.CharField(max_length = 50)

    class Meta:
        verbose_name = 'Phases'
        verbose_name_plural = 'Phases'

def get_path(instance  , file_name):
    return 'static/applications/'+str(instance.resident.resident_id)+"/"+str(instance.application_id)+"/"+file_name



class Document(models.Model):
    document_id  = models.AutoField(primary_key = True)
    # File Info

    resident = models.ForeignKey(
        Resident,
        on_delete = models.CASCADE,
    )
    application_id = models.IntegerField(null = True, blank = True)

    file = models.FileField(upload_to = get_path ,null = True, blank = True)
    file_name = models.CharField(max_length = 100, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    date_uploaded  = models.DateTimeField(null = True, blank = True)

    class Meta:
        verbose_name = 'Documents'
        verbose_name_plural = 'Documents'


class Confirmation(models.Model):
    confirmation_id  = models.AutoField(primary_key = True)

    confirmation_document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
    )

    description = models.CharField(max_length = 100, null = True, blank = True)
    date_uploaded  = models.DateTimeField(null = True, blank = True)

    class Meta:
        verbose_name = 'Confirmations'
        verbose_name_plural = 'Confirmations'

class Application(models.Model):

    application_id = models.AutoField(primary_key = True)

    resident = models.ForeignKey(
        Resident,
        on_delete = models.CASCADE,
    )

    phase = models.ForeignKey(
        Phase,
        on_delete = models.CASCADE,
    )

    # Application Prerequisites
    appointment_date = models.DateTimeField(null = True, blank = True)
    medicaid_eligible = models.CharField(max_length = 50,null = True, blank = True)

    # Application Type Info
    ltc = models.CharField(max_length = 50,null = True, blank = True)
    spousal = models.CharField(max_length = 50,null = True, blank = True)
    application_type = models.CharField(max_length = 50, null = True, blank = True)

    # Application Info
    date_of_application_submission  = models.DateTimeField(null = True, blank = True)
    date_of_application_submission_deadline  = models.DateTimeField(null = True, blank = True)
    medicaid_pickup_date = models.DateTimeField(null = True, blank = True)
    estimated_nami = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank = True)
    copay  = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank = True)
    copay_start_date =  models.DateTimeField(null = True, blank = True)
    secondary_pays_copay  = models.DecimalField(max_digits=10,decimal_places=2,null = True, blank = True)
    application_state = models.CharField(max_length = 50, null = True, blank = True)
    application_county = models.CharField(max_length = 50, null = True, blank = True)
    spousal_refusal= models.CharField(max_length = 50,null = True, blank = True)
    initial_response = models.CharField(max_length = 20, null = True, blank = True)

    #DSS Contact Info
    dss_contact_address  = models.CharField(max_length = 100, null = True, blank = True)
    dss_contact_phone  = models.CharField(max_length = 100, null = True, blank = True)
    dss_contact_email = models.EmailField(max_length = 100, null = True, blank = True)
    dss_contact_fax  = models.CharField(max_length = 100, null = True, blank = True)

    tracking_status = models.BooleanField(null = True, blank = True)

    application_document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
        null = True,
    )

    application_confirmation = models.ForeignKey(
        Confirmation,
        on_delete = models.CASCADE,
        null = True,
    )
    # date_of_medicaid_approval  = models.DateTimeField(null = True, blank = True)
    # date_of_medicaid_recertification  = models.DateTimeField(null = True, blank = True)



    # approval_notice_date = models.DateTimeField(null = True, blank = True)



    # approval_verified  = models.BooleanField(null = True, blank = True)
    # fair_hearing_required  = models.CharField(max_length = 50,null = True, blank = True)
    # fair_hearing_notice_date = models.DateTimeField(null = True, blank = True)


    class Meta:
        verbose_name = 'Applications'
        verbose_name_plural = 'Applications'




class ResponseType(models.Model):
    # Response Type Definitions
    response_type_id  = models.AutoField(primary_key = True)
    response_type = models.CharField(max_length = 50,  null = True, blank=True)

    class Meta:
        verbose_name = 'Response Types'
        verbose_name_plural = 'Response Types'


class Response(models.Model):
    response_id = models.AutoField(primary_key = True)

    application = models.ForeignKey(
        Application,
        on_delete = models.CASCADE,
    )

    response_type = models.ForeignKey(
        ResponseType,
        on_delete  = models.CASCADE,
        null = True,
    )

    document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
        null = True,
    )

    response_date = models.DateField(null = True ,blank= True)

    class Meta:
        verbose_name = 'Responses'
        verbose_name_plural = 'Responses'



class RFI(models.Model):
    rfi_id  = models.AutoField(primary_key = True)

    response = models.ForeignKey(
        Response,
        on_delete = models.CASCADE,
    )

    document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
        null = True,
    )

    rfi_due_date  = models.DateTimeField(null = True, blank = True)

    rfi_extension_request = models.CharField(max_length = 50,  null = True, blank=True)
    rfi_extension_response= models.CharField(max_length = 50,  null = True, blank=True)

    rfi_documentation_submitted= models.CharField(max_length = 50,  null = True, blank=True)
    rfi_documentation_submitted_date = models.DateField(null = True , blank = True)

    rfi_response = models.CharField(max_length = 20, null = True, blank = True)

    class Meta:
        verbose_name = 'RFIS'
        verbose_name_plural = 'RFIS'


class Approval(models.Model):

    approval_id  = models.AutoField(primary_key = True)

    response = models.ForeignKey(
        Response,
        on_delete = models.CASCADE,
    )

    document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
        null = True,
    )

    approval_start_date = models.DateTimeField(null = True, blank = True)
    approval_end_date = models.DateTimeField(null = True, blank = True)
    approval_recertification_date = models.DateTimeField(null = True, blank = True)
    approval_notice_date  = models.DateTimeField(null = True, blank = True)
    satisfied_with_approval = models.CharField(max_length = 50,  null = True, blank=True)
    fair_hearing_required = models.CharField(max_length = 50,  null = True, blank=True)

    class Meta:
        verbose_name = 'Approvals'
        verbose_name_plural = 'Approvals'

class Denial(models.Model):
    denial_id  = models.AutoField(primary_key = True)

    response = models.ForeignKey(
        Response,
        on_delete = models.CASCADE,
    )

    document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
        null = True,
    )

    class Meta:
        verbose_name = 'Denials'
        verbose_name_plural = 'Denials'

class NAMI(models.Model):
    nami_id  = models.AutoField(primary_key = True)

    approval = models.ForeignKey(
        Approval,
        on_delete = models.CASCADE,
    )

    nami_start_date  = models.DateField(null = True, blank = True)
    nami_end_date  = models.DateField(null = True, blank = True)
    nami_amount = models.FloatField(null = True, blank = True)

    class Meta:
        verbose_name = 'NAMIS'
        verbose_name_plural = 'NAMIS'


class AlertType(models.Model):
    alert_type_id = models.AutoField(primary_key = True)
    alert_name = models.CharField(max_length = 50,  null = False, blank=False)

class Alert(models.Model):
    alert_id = models.AutoField(primary_key = True)
    resident = models.ForeignKey(
        Resident,
        on_delete = models.CASCADE,
        null = True,
    )
    application = models.ForeignKey(
        Application,
        on_delete = models.CASCADE,
        null = True,
    )

    alert_type = models.ForeignKey(
        AlertType,
        on_delete = models.CASCADE,
    )

    alert_priority = models.IntegerField(null=False,blank=False)
    alert_status =models.BooleanField(default = False)

    class Meta:
        verbose_name = 'Alerts'
        verbose_name_plural = 'Alerts'

class FairHearing(models.Model):
    fair_hearing_id = models.AutoField(primary_key = True)

    application = models.ForeignKey(
        Application,
        on_delete = models.CASCADE,
        null = True,
    )

    fair_hearing_date = models.DateField(null = True, blank = True)
    fair_hearing_time =  models.TimeField(null = True, blank = True)
    fair_hearing_address = models.CharField(max_length = 50,  null = True, blank=True)
    fair_hearing_outcome = models.CharField(max_length = 50,  null = True, blank=True)
    fair_hearing_appeal = models.CharField(max_length = 50,  null = True, blank=True)



# class Snowden(models.Models):
#     log_id = models.BigAutoField(primary_key = True)\

#     user = models.ForeignKey(
#         Users,
#         on_delete = models.CASCADE,
#     )

#     application = models.ForeignKey(
#         Application,
#         on_delete = models.CASCADE,
#     )
#     table_name = models.CharField(max_length = 50)
#     column_name = models.CharField(max_lenth = 50)
#     old_value  = models.CharField(max_lenth = 250)
#     new_value  = models.CharField(max_lenth = 250)
#     log_ip = models.CharField(max_length = 15)
#     date = models.DateTimeField(auto_now_add = True)
