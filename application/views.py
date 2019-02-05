from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import NameForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .additionalInfo import AdditionalInfo
from datetime import datetime, timedelta
from django.http import JsonResponse
from calendar import monthrange


def application_tracking(request):
    application = requests.GET["application_id"]

def track_untrack_resident(request):
    requested_resident_id = request.GET['row_id']
    track = request.GET['tracking']

    requested_resident_id = int(requested_resident_id)
    resident = Resident.objects.get(resident_id = requested_resident_id)


    if track == "true":
        # Audit Log
        Snowden.objects.create(user = request.user,table_name = resident._meta.verbose_name,row_id = resident.resident_id,column_name = "tracking_status",old_value = getattr(resident,"tracking_status") if getattr(resident,"tracking_status") is not None else "None",new_value = "True",log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())
        resident.tracking_status = True

        # Audit Log
        Snowden.objects.create(user = request.user,table_name = resident._meta.verbose_name,row_id = resident.resident_id,column_name = "dismiss",old_value = getattr(resident,"dismiss") if getattr(resident,"dismiss") is not None else "None",new_value = "True",log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())
        resident.dismiss = True

        if not Application.objects.filter(resident_id = requested_resident_id).exists():
            application = Application.objects.create(resident = resident, phase = Phase.objects.get(phase_id = 1),tracking_status = True)
            # Audit Log
            Snowden.objects.create(
                user = request.user,
                table_name = application._meta.verbose_name,
                row_id = application.application_id,
                column_name = "Object Created",
                old_value = "None",
                new_value = resident.resident_id,
                log_ip = request.META.get('REMOTE_ADDR'),
                date = datetime.now()
            )

        resident.save()

    elif track == "false":

        # Audit Log
        Snowden.objects.create(user = request.user,table_name = resident._meta.verbose_name,row_id = resident.resident_id,column_name = "tracking_status",old_value = getattr(resident,"tracking_status") if getattr(resident,"tracking_status") is not None else "None",new_value = "False",log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())
        resident.tracking_status = False

        # Audit Log
        Snowden.objects.create(user = request.user,table_name = resident._meta.verbose_name,row_id = resident.resident_id,column_name = "dismiss",old_value = getattr(resident,"dismiss") if getattr(resident,"dismiss") is not None else "None",new_value = "True",log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())

        resident.dismiss = True
        resident.save()
    return HttpResponse("200")

'''REASON FOR ANNOYING ERROR'''
def approval_verified(request):
    if request.method == 'GET':
        resident_id =int(request.GET['resident_id'])

        application = Application.objects.get(resident = resident_id)

        if request.GET['approval_verified'] == "true":
            application.approval_verified = True
            application.save()
        else:
            application.approval_verified = False
            application.save()
        # Sending an success response
        return HttpResponse("200")
    else:
        return HttpResponse("Request method is not a GET")


def update_resident(request):
    resident_id =int(request.GET['resident_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    resident = Resident.objects.get(resident_id = resident_id)

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = resident._meta.verbose_name,
        row_id = str(resident_id),
        column_name = column,
        old_value = str(getattr(resident,column)) if getattr(resident,column) is not None else "None",
        new_value = str(new_value),
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

    field = setattr(resident, column,new_value)
    resident.save()

    return HttpResponse("200")

def update_application(request):
    application_id =int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    application = Application.objects.get(application_id = application_id)

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = application._meta.verbose_name,
        row_id = application_id,
        column_name = column,
        old_value = getattr(application,column) if getattr(application,column) is not None else "None",
        new_value = new_value if new_value is not None else "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    field = setattr(application,column,new_value)


    if column == "medicaid_pickup_date":

        pick_up_date = datetime.strptime(application.medicaid_pickup_date, '%Y-%m-%d')
        application_due_date = monthrange((pick_up_date + timedelta(days = 90)).year,(pick_up_date + timedelta(days = 90)).month)[1]
        date = pick_up_date+timedelta(days =(90 +application_due_date-(pick_up_date+timedelta(days = 90)).day))
        
        Snowden.objects.create(
            user = request.user,
            table_name = application._meta.verbose_name,
            row_id = application_id,
            column_name = "date_of_application_submission_deadline",
            old_value = getattr(application,"date_of_application_submission_deadline") if getattr(application,"date_of_application_submission_deadline") is not None else "None",
            new_value = date.strftime("%Y-%m-%d"),
            log_ip = request.META.get('REMOTE_ADDR'),
            date = datetime.now()
        )
        application.date_of_application_submission_deadline = date.strftime("%Y-%m-%d")
        application.save()
        return HttpResponse(date.strftime("%Y-%m-%d"))
    else:
        application.save()
        return HttpResponse("200")

def update_confirmation(request):
    confirmation_id =int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    confirmation = Confirmation.objects.get(confirmation_id = confirmation_id)

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = confirmation._meta.verbose_name,
        row_id = confirmation_id,
        column_name = column,
        old_value = getattr(confirmation,column) if getattr(confirmation,column) is not None else "None",
        new_value = new_value if new_value is not None else "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

    field = setattr(confirmation,column,new_value)
    confirmation.save()

    return HttpResponse("200")

def update_alert(request):
    alert_id = int(request.GET['alert_id'])
    alert = Alert.objects.get(alert_id = alert_id)
    field = setattr(alert, "alert_status",True)
    alert.save()
    # Sending an success response
    return HttpResponse("200")

def phase_change(request):
    # Sending an success response
    application_id =int(request.GET['application_id'])
    phase_id =int(request.GET['phase_id'])

    application = Application.objects.get(application_id = application_id)
    phase = Phase.objects.get(phase_id = phase_id)


    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = application._meta.verbose_name,
        row_id = application_id,
        column_name = "Phase",
        old_value = getattr(application,"phase_id") if getattr(application,"phase_id") is not None else "None",
        new_value = phase_id,
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    application.phase = phase
    application.save()
    return HttpResponse(str(phase.phase_name))

def create_response(request):
    application_id = int(request.GET['application_id'])
    response_type = request.GET['response_type']
    if response_type != "not_received":
        response = Response.objects.create(application_id = application_id, response_type = ResponseType.objects.get(response_type = response_type))

        # Audit Log
        Snowden.objects.create(user = request.user,table_name = response._meta.verbose_name,row_id = response.response_id,column_name = "Object Created",old_value = "None",new_value = application_id,log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())

        if response_type == 'rfi':
            action = RFI.objects.create(response = response)
            return_info = action.rfi_id
        elif response_type == 'approved':
            action = Approval.objects.create(response = response)
            return_info = action.approval_id
        elif response_type == 'denied':
            action = Denial.objects.create(response = response)
            return_info = action.denial_id

        # Audit Log
        Snowden.objects.create(user = request.user,table_name = action._meta.verbose_name,row_id = action.response_id,column_name = "Object Created",old_value = "None",new_value = response.response_id,log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())

        # return HttpResponse({"return_info":return_info, "response_id":response.response_id})
        return JsonResponse([response.response_id, return_info], safe=False)
    else:
        #Audit Log
        Snowden.objects.create(user = request.user,table_name = "None",row_id = application_id ,column_name = "Switched to Not Recieved",old_value = "None",new_value = "None",log_ip = request.META.get('REMOTE_ADDR'),date = datetime.now())
        return HttpResponse('no response created for not_received')


def update_rfi(request):
    rfi_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    rfi = RFI.objects.get(rfi_id = rfi_id)

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = rfi._meta.verbose_name,
        row_id = rfi_id,
        column_name = column,
        old_value = getattr(rfi,column) if getattr(rfi,column) is not None else "None",
        new_value = new_value if new_value is not None else "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

    field = setattr(rfi, column,new_value)
    rfi.save()
    return HttpResponse("200")

def update_denial(request):
    denial_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    denial = Denial.objects.get(denial_id = denial_id)

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = denial._meta.verbose_name,
        row_id = denial_id,
        column_name = column,
        old_value = getattr(denial,column) if getattr(denial,column) is not None else "None",
        new_value = new_value if new_value is not None else "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

    field = setattr(denial, column,new_value)
    denial.save()
    return HttpResponse("200")

def update_approval(request):
    approval_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    approval = Approval.objects.get(approval_id = approval_id)
    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = approval._meta.verbose_name,
        row_id = approval_id,
        column_name = column,
        old_value = getattr(approval,column) if getattr(approval,column) is not None else "None",
        new_value = new_value if new_value is not None else "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    field = setattr(approval, column,new_value)
    approval.save()
    return HttpResponse("200")

def create_nami(request):
    approval_id = int(request.GET['approval_id'])
    nami = NAMI.objects.create(approval = Approval.objects.get(approval_id = approval_id))
    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = nami._meta.verbose_name,
        row_id = nami.nami_id,
        column_name = 'Object Created',
        old_value = "None",
        new_value = approval_id,
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    return HttpResponse(int(nami.nami_id))

def update_nami(request):
    nami_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    nami = NAMI.objects.get(nami_id = nami_id)
    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = nami._meta.verbose_name,
        row_id = nami_id,
        column_name = column,
        old_value = getattr(nami,column) if getattr(nami,column) is not None else "None",
        new_value = new_value if new_value is not None else "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    field = setattr(nami, column,new_value)
    nami.save()
    return HttpResponse("200")

def delete_nami(request):
    nami_id = int(request.GET['row_id'])
    nami = NAMI.objects.get(nami_id = nami_id)
    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = nami._meta.verbose_name,
        row_id = nami.nami_id,
        column_name = "Object Deleted",
        old_value = nami.nami_id,
        new_value = "None",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    nami.delete()
    return HttpResponse("200")

def create_application(request):
    resident_id = int(request.GET['resident_id'])
    application = Application.objects.create(resident = Resident.objects.get(resident_id = resident_id), phase = Phase.objects.get(phase_id = 1))

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = application._meta.verbose_name,
        row_id = application.application_id,
        column_name = "Object Created",
        old_value = "None",
        new_value = resident_id,
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    return HttpResponse(int(application.application_id))

def delete_response(request):
    response_type = request.GET['response_type']
    response_id = int(request.GET['response_id'])
    if response_type == "rfi":
        object = RFI.objects.get(rfi_id = response_id)
        object.delete()
    elif response_type == "denial":
        object = Denial.objects.get(denial_id = response_id)
        object.delete()
    elif response_type == "approval":
        object = Approval.objects.get(approval_id = response_id)
        object.delete()

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = object._meta.verbose_name,
        row_id = response_id,
        column_name = "Object Deleted",
        old_value = "DELETED",
        new_value = "DELETED",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    return HttpResponse("200")

def create_fair_hearing(request):
    response_id = int(request.GET['response_id'])
    fair_hearing = FairHearing.objects.create(response = Response.objects.get(response_id = response_id))


    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = fair_hearing._meta.verbose_name,
        row_id = fair_hearing.fair_hearing_id,
        column_name = "Object Created",
        old_value = "None",
        new_value = response_id,
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

    return HttpResponse(int(fair_hearing.fair_hearing_id))

def update_fair_hearing(request):
    fair_hearing_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    fair_hearing = FairHearing.objects.get(fair_hearing_id = fair_hearing_id)

    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = fair_hearing._meta.verbose_name,
        row_id = fair_hearing_id,
        column_name = column,
        old_value = getattr(fair_hearing,column) if getattr(fair_hearing,column) is not None else "None",
        new_value = new_value,
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

    field = setattr(fair_hearing, column,new_value)
    fair_hearing.save()
    return HttpResponse("200")

def delete_fair_hearing(request):
    fair_hearing_id = int(request.GET['row_id'])
    fair_hearing = FairHearing.objects.get(fair_hearing_id = fair_hearing_id)
    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = fair_hearing._meta.verbose_name,
        row_id = fair_hearing_id,
        column_name = "Object Deleted",
        old_value = "DELETED",
        new_value = "DELETED",
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )
    fair_hearing.delete()
    return HttpResponse("200")
