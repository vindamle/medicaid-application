from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import NameForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Resident, ApplicationTracking, Alert, AlertType,Phase
from .additionalInfo import AdditionalInfo

def update_list(request):
    if request.method == 'GET':
        requested_resident_id = request.GET['resident_id']
        track = request.GET['tracking']
        requested_resident_id = int(requested_resident_id)
        resident = Resident.objects.get(resident_id = requested_resident_id)


        if track == "true":
            resident.tracking_status = True
            resident.dismiss = True
            if not ApplicationTracking.objects.filter(resident_id = requested_resident_id).exists():

                resident.phase = Phase.objects.get(phase_id = 1)
                application = ApplicationTracking(resident = resident)
                application.save()
            resident.save()


            # resident_info = AdditionalInfo()
        elif track == "false":
            resident.tracking_status = False
            resident.save()
        return HttpResponse("200")
    else:
        return HttpResponse("Request method is not a GET")

def approval_verified(request):
    if request.method == 'GET':
        resident_id =int(request.GET['resident_id'])

        application = ApplicationTracking.objects.get(resident = resident_id)

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

    resident_id =int(request.GET['resident_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']

    resident = Resident.objects.get(resident_id = resident_id)
    application = ApplicationTracking.objects.get(resident = resident)

    field = setattr(application,column,new_value)
    application.save()

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
    resident_id =int(request.GET['resident_id'])
    phase_id =int(request.GET['phase_id'])
    resident = Resident.objects.get(resident_id = resident_id)
    phase = Phase.objects.get(phase_id = phase_id)
    resident.phase = phase
    resident.save()

    return HttpResponse(str(phase.phase_name))

def create_rfi(request):
    resident_id =int(request.GET['resident_id'])
    application_id = int(request.GET['application_id'])
    RFI = RFI(resident_id = resident_id, application_id = application_id)
    RFI.save()
    return HttpResponse(str(RFI.rfi_id))


def update_rfi(request):

    rfi_id = int(request.GET['rfi_id'])
    column =request.GET['column']
    new_value =request.GET['new_value']
    RFI = RFI.objects.get(rfi_id = rfi_id)
    field = setattr(RFI, column,new_value)
    RFI.save()
    return HttpResponse("200")
