from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import NameForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .additionalInfo import AdditionalInfo


def application_tracking(request):
    application = requests.GET["application_id"]

def track_untrack_resident(request):
    requested_resident_id = request.GET['row_id']
    track = request.GET['tracking']

    requested_resident_id = int(requested_resident_id)
    resident = Resident.objects.get(resident_id = requested_resident_id)


    if track == "true":
        resident.tracking_status = True
        resident.dismiss = True
        if not Application.objects.filter(resident_id = requested_resident_id).exists():
            application = Application(resident = resident, phase = Phase.objects.get(phase_id = 1),tracking_status = True)
            application.save()
        resident.save()

    elif track == "false":
        resident.tracking_status = False
        resident.dismiss = True
        resident.save()
    return HttpResponse("200")


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
    field = setattr(application,column,new_value)
    application.save()
    return HttpResponse("200")

def update_confirmation(request):
    confirmation_id =int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    confirmation = Confirmation.objects.get(confirmation_id = confirmation_id)

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
    application.phase = phase
    application.save()
    return HttpResponse(str(phase.phase_name))

def create_response(request):
    application_id = int(request.GET['application_id'])
    response_type = request.GET['response_type']
    if response_type != "not_received":
        response = Response.objects.create(application_id = application_id, response_type = ResponseType.objects.get(response_type = response_type))
        if response_type == 'rfi':
            rfi = RFI.objects.create(response = response)
            return_info = rfi.rfi_id
        elif response_type == 'approved':
            approval = Approval.objects.create(response = response)
            return_info = approval.approval_id
        elif response_type == 'denied':
            denial = Denial.objects.create(response = response)
            return_info = denial.denial_id
        return HttpResponse(return_info)
    else:
        return HttpResponse('no response created for not_received')

def update_rfi(request):
    rfi_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    if new_value == '':
        new_value = None
    rfi = RFI.objects.get(rfi_id = rfi_id)
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
    field = setattr(approval, column,new_value)
    approval.save()
    return HttpResponse("200")

def create_nami(request):
    approval_id = int(request.GET['approval_id'])
    nami = NAMI.objects.create(approval = Approval.objects.get(approval_id = approval_id))
    return HttpResponse(int(nami.nami_id))

def update_nami(request):
    nami_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    nami = NAMI.objects.get(nami_id = nami_id)
    field = setattr(nami, column,new_value)
    nami.save()
    return HttpResponse("200")

def delete_nami(request):
    nami_id = int(request.GET['row_id'])
    nami = NAMI.objects.get(nami_id = nami_id)
    nami.delete()
    return HttpResponse("200")

def create_application(request):
    resident_id = int(request.GET['resident_id'])
    application = Application.objects.create(resident = Resident.objects.get(resident_id = resident_id), phase = Phase.objects.get(phase_id = 1))
    return HttpResponse(int(application.application_id))

def delete_response(request):
    response_type = request.GET['response_type']
    response_id = int(request.GET['response_id'])
    if response_type == "rfi":
        rfi = RFI.objects.get(rfi_id = response_id)
        rfi.delete()
    elif response_type == "denial":
        denial = Denial.objects.get(denial_id = response_id)
        denial.delete()
    elif response_type == "approval":
        approval = Approval.objects.get(approval_id = response_id)
        approval.delete()
    return HttpResponse("200")

def create_fair_hearing(request):
    response_id = int(request.GET['response_id'])
    fair_hearing = FairHearing.objects.create(response = Response.objects.get(response_id = response_id))
    return HttpResponse(int(fair_hearing.fair_hearing_id))

def update_fair_hearing(request):
    fair_hearing_id = int(request.GET['row_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    fair_hearing = FairHearing.objects.get(fair_hearing_id = fair_hearing_id)
    field = setattr(fair_hearing, column,new_value)
    fair_hearing.save()
    return HttpResponse("200")

def delete_fair_hearing(request):
    fair_hearing_id = int(request.GET['row_id'])
    fair_hearing = FairHearing.objects.get(fair_hearing_id = fair_hearing_id)
    fair_hearing.delete()
    return HttpResponse("200")

