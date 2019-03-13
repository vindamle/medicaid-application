from django.db import models
from pathlib import Path
from django.contrib.auth.models import User
from pgcrypto_expressions.fields import EncryptedCharField
# Create your models here.

class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_pcc_id= models.IntegerField(null=True, blank=True)
    facility_name = models.CharField(max_length = 100, null=True, blank=True)
    facility_code = models.CharField(max_length = 10, null=True, blank=True)

    def __str__(self):
        return self.facility_name

    class Meta:
        verbose_name = 'Facilities'
        verbose_name_plural = 'Facilities'

class Resident(models.Model):
    resident_id  = models.BigAutoField(primary_key=True)
    resident_number = models.IntegerField(null = True, blank = True)

    #Patient Info
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    ssn = EncryptedCharField(max_length=50, null=True, blank=True)
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
    medicaid_pickup_date = models.DateField(null = True, blank = True)
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

    application_creation_date = models.DateField(auto_now_add = True)
    # date_of_medicaid_approval  = models.DateTimeField(null = True, blank = True)
    # date_of_medicaid_recertification  = models.DateTimeField(null = True, blank = True)



    # approval_notice_date = models.DateTimeField(null = True, blank = True)



    approval_verified  = models.BooleanField(null = True, blank = True)
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
    approval_satisfied = models.CharField(max_length = 50,  null = True, blank=True)
    approval_contacted_dss =  models.CharField(max_length = 50,  null = True, blank=True)
    approval_resolved_through_dss =  models.CharField(max_length = 50,  null = True, blank=True)
    approval_fair_hearing_required = models.CharField(max_length = 50,  null = True, blank=True)

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

    denial_notice_date = models.DateTimeField(null = True, blank = True)
    denial_fair_hearing_requested = models.CharField(max_length = 50, null = True, blank = True)
    denial_documentation_submitted = models.CharField(max_length = 50, null = True, blank = True)
    denial_contacted_dss =  models.CharField(max_length = 50,  null = True, blank=True)
    denial_resolved_through_dss =  models.CharField(max_length = 50,  null = True, blank=True)

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
    alert_priority = models.IntegerField(null=False,blank=False)
    alert_class = models.CharField(max_length = 15,  null = True, blank=False)

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
    alert_status =models.BooleanField(default = False)

    trigger_date = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name = 'Alerts'
        verbose_name_plural = 'Alerts'

class FairHearing(models.Model):
    fair_hearing_id = models.AutoField(primary_key = True)

    response = models.ForeignKey(
        Response,
        on_delete = models.CASCADE,
        null = True,
    )

    fair_hearing_outcome_document = models.ForeignKey(
        Document,
        on_delete = models.CASCADE,
        null = True,
    )

    fair_hearing_confirmation = models.ForeignKey(
        Confirmation,
        on_delete = models.CASCADE,
        null = True,
    )

    fair_hearing_date = models.DateField(null = True, blank = True)
    fair_hearing_time =  models.TimeField(null = True, blank = True)
    fair_hearing_address = models.CharField(max_length = 50,  null = True, blank=True)
    fair_hearing_outcome = models.CharField(max_length = 50,  null = True, blank=True)

    fair_hearing_representative_type = models.CharField(max_length = 50,  null = True, blank=True)
    fair_hearing_representative_name = models.CharField(max_length = 100,  null = True, blank=True)

    fair_hearing_satisfied = models.CharField(max_length = 10,  null = True, blank=True)
    fair_hearing_outcome_date = models.DateField(null = True, blank = True)

    class Meta:
        verbose_name = 'Fair Hearings'
        verbose_name_plural = 'Fair Hearings'

class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    class Meta:
        permissions = (
            ("Boro Park","Boro Park"),
            ("Brooklyn","Brooklyn"),
            ("Bushwick","Bushwick"),
            ("Washington","Washington"),
            ("Corning","Corning"),
            ("Argyle Center","Argyle Center"),
            ("Bronx","Bronx"),
            ("Warren","Warren"),
            ("Deptford","Deptford"),
            ("Oak Hill","Oak Hill"),
            ("Beth Abraham","Bet Abraham"),
            ("Essex","Essex"),

            ("Far Rockaway","Far Rockaway"),
            ("Fulton","Fulton"),
            ("Carthage","Carthage"),
            ("Hammonton","Hammonton"),
            ("Holliswood","Holliswood"),
            ("Hope Center","Hope Center"),
            ("WC - Elm Manor","WC - Elm Manor"),
            ("Mount Laurel","Mount Laurel"),
            ("N. Manor","Northern Manor"),
            ("Ellicott","Ellicott Center"),
            ("N. Metropolitan","N. Metropolitan"),
            ("Glens Falls","Glens Falls"),
            ("N. Riverview","N. Riverview"),
            ("New Paltz","New Paltz"),
            ("Ontario Center","Ontario Center"),
            ("Ontario County","Ontario County"),
            ("STBN County","STBN County"),
            ("Onondaga","Onondaga"),
            ("PG - Quality Care","Quality Care"),
            ("PG - Stamford Residence","Stamford Residence"),
            ("PG - Walnut Hills","Walnut Hills"),
            ("PG - Westview Manor","Westview Manor"),
            ("Claremont ALP","Claremont"),
            ("Steuben","Steuben"),
            ("Suffolk","Suffolk"),
            ("University","University"),
            ("Williamsbridge","Williamsbridge"),
            ("Bannister","Bannister"),
            ("Buffalo","Buffalo"),
            ("Park View","Park View"),
            ("Schenectady","Schenectady"),
            ("Slate Valley","Slate Valley"),
            ("Triboro (ALP)","Alpine Triboro Center"),
            ("Triboro Center","Triboro Center"),
            ("Troy","Troy"),
            ("Centers for Care","Centers for Care"),
            ("Brookside - MA","Brookside"),
            ("Granville","Granville"),
            ("Evolve","Evolve"),
            ("Kingston","Kingston"),
            ("New Boston","New Boston"),
            ("WC - Wedgewood","Wedgewood"),
            ("Cooperstown","Cooperstown"),
            ("Martine","Martine"),
            ("Focus - Otsego - Charts","Otsego"),
            ("Focus - Utica - Charts","Utica"),
            ("EC - Midwest","Midwest"),
            ("EC - Southwest","Southwest Center"),
            ("Mills Pond","Mills Pond"),
            ("Sayville","Sayville"),
            ("Birchwood - VT","Birchwood"),
            ("WC - Folts ADC","Folts ADC"),
            ("EC - Tulsa","Tulsa"),
            ("EC - Claremore","Claremore"),
            ("EC - Memory Care","Memory Care"),
            ("Castle Senior Living","Castle Senior Living"),
            ("Focus Senior Living","Focus Senior Living"),
            ("Richmond (Staten Island)","Richmond Center"),
            ("WC - Folts Home","Folts Home"),
            ("Creekview","Creekview"),
            ("EC - Crystal","Crystal Center"),
            ("EC - Pikeville","Pikeville"),
            ("Kansas City ALF","Kansas City ALF"),
            ("Overland Park ALF","Overland Park ALF"),
            ("Oneida Center","Oneida Center"),
            ("Butler Center","Butler Center"),
            ("Kansas City","Kansas City"),
            ("Overland Park","Overland Park"),
            ("Ten Broeck","Ten Broeck"),
            ("Topeka Center","Topeka Center"),
            ("Wichita Center","Wichita Center"),

        )

        verbose_name = 'Employees'
        verbose_name_plural = 'Employees'

class Snowden(models.Model):
    log_id = models.BigAutoField(primary_key = True)

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )

    row_id = models.IntegerField()
    table_name = models.CharField(max_length = 50)
    column_name = models.CharField(max_length = 50)
    old_value  = models.CharField(max_length = 250)
    new_value  = models.CharField(max_length = 250)
    log_ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Edward Snowden'
        verbose_name_plural = 'Edward Snowden'
