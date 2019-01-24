from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .forms import ApplicationForm, UploadFileForm
from application.models import *
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

from django.contrib.auth.models import Permission

# Pending View
# Shows List of All Currently Tracked Applications
class PendingView(View):
    template_name = "pending.html"
    #Returns Applcations with status of track set to True
    def get(self, request, *args, **kwargs):
        applications  = list()
        if request.user.is_authenticated:
            permissions = Permission.objects.filter(user = request.user)
            for permission in permissions:

                apps = Application.objects.filter(tracking_status = True, resident__tracking_status = True,resident__facility_name =permission.codename)
                for app in apps:
                    applications.append(app)

            return render(request,self.template_name, {'applications':applications})
        else:
            return redirect('login')


# ActivityView
# Shows Lists of all residents that have not been tracked or untracked
class ActivityView(View):

    template_name = "activity.html"

    #Returns Residents with new activitys that have not been tracked/not tracked
    def get(self, request, *args, **kwargs):

        new_admission = []
        payor_change = []
        discharge = []

        if request.user.is_authenticated:
            permissions = Permission.objects.filter(user = request.user)

            for permission in permissions:
                print(permission)

                new_admits = Resident.objects.filter(facility_name =permission.codename, tracking_status = None, activity_type = 'A')
                for new_admit in new_admits:
                    new_admission.append(new_admit)

                new_payor_changes = Resident.objects.filter(facility_name =permission.codename,activity_type = 'P', dismiss = False)
                for new_payor_change in new_payor_changes:
                    payor_change.append(new_payor_change)

                new_discharges= Resident.objects.filter(facility_name =permission.codename,tracking_status = None, activity_type = 'D')
                for new_discharge in new_discharges:
                    discharge.append(new_discharge)
                print(len(new_admission))
            return render(request,self.template_name, {'discharge':discharge,'admission':new_admission,'payor_change':payor_change})
        else:
            return redirect('login')



class PendingAlertsView(View):
    form_class = ApplicationForm
    template_name = "pending_alerts.html"
    list = []
    tracklist = []


    def get(self, request, *args, **kwargs):


        if request.user.is_authenticated:
            permissions = Permission.objects.filter(user = request.user)
            for permission in permissions:
                residents = Resident.objects.filter(facility_name =permission.codename, tracking_status = True)
                self.list = list()
                for resident in residents:

                    alerts = Alert.objects.filter(resident = resident , alert_status = False)

                    for alert in alerts:
                        self.list.append(alert)

                return render(request,self.template_name, {'alerts':self.list,"form":self.form_class})
        else:
            return redirect('login')



class ShowView(View):
    form_class = UploadFileForm
    template_name = "show.html"




    def get(self, request, *args, **kwargs):
        '''if GET  '''

        resident_id= int(request.GET["resident_id"])
        resident = Resident.objects.get(resident_id = resident_id)
        applications = Application.objects.filter(resident = Resident.objects.get(resident_id = resident_id))


        resident_alerts = Alert.objects.filter(resident = Resident.objects.get(resident_id = resident_id), alert_status = False)

        # documents = Document.objects.filter(resident_id = resident_id)
        rfis = RFI.objects.filter(response__application__resident__resident_id = resident_id).order_by('response__application__application_id','rfi_id')
        denials = Denial.objects.filter(response__application__resident__resident_id = resident_id).order_by('response__application__application_id','denial_id')
        approvals = Approval.objects.filter(response__application__resident__resident_id = resident_id).order_by('response__application__application_id','approval_id')
        namis = NAMI.objects.filter(approval__response__application__resident__resident_id = resident_id).order_by('approval__approval_id', 'nami_id')
        # medicaid_application_documents = Document.objects.filter(resident_id = resident_id, description = "medicaid_application")
        # rfi_documents = Document.objects.filter(resident_id = resident_id, description = "rfi").order_by('rfi_id')
        # applications = results
        # print(application)
        # return render(request,self.template_name, {'rfis':rfis,'documents':documents,'resident':resident,'applications':applications,"resident_alerts":resident_alerts, 'medicaid_application_documents': medicaid_application_documents, "rfi_documents":rfi_documents, "form":self.form_class})
        return render(request, self.template_name, {'resident': resident, 'applications':applications, 'rfis':rfis, 'denials': denials, 'approvals': approvals, 'namis': namis, 'resident_alerts': resident_alerts})
    def post(self, request, *args, **kwargs):


        file = request.FILES.getlist('document')
        type = request.POST.get('file_type')
        application_id = request.POST.get('application_id')
        resident_id = request.POST.get('resident_id')


        ROOT = Path.cwd()
        path = Path(str(ROOT) + "/static/applications/"+resident_id+"/"+str(application_id))
        if not path.exists():
            print("Create Path")
            path.mkdir(parents=True, exist_ok = True)

        try:

            new_document = Document.objects.create(
                resident = Resident.objects.get(resident_id = request.POST.get('resident_id')),
                application_id = application_id,
                file = file[0],
                file_name = (file[0].name).split(".")[0],
                description = type,
                date_uploaded = datetime.now(),
            )
        except Exception as e:
            print("\n\n",str(e),"\n\n")

        if type  == 'medicaid_application':
            application = Application.objects.get(application_id = int(application_id))
            application.application_document = new_document
            application.save()
        elif type == 'rfi':
            rfi = RFI.objects.get(rfi_id = int(request.POST.get('rfi_id')))
            rfi.document_id = new_document.document_id
            rfi.save()
        elif type == 'approval':
            approval = Approval.objects.get(approval_id = int(request.POST.get('approval_id')))
            approval.document_id = new_document.document_id
            approval.save()
        elif type == 'application_confirmation':
            confirmation = Confirmation.objects.create(confirmation_document = new_document, description = type)
            application = Application.objects.get(application_id = int(application_id))
            application.application_confirmation = confirmation
            application.save()

        return redirect('/show/?resident_id={}'.format(str(resident_id)))



class ApprovalsView(View):
    form_class = ApplicationForm
    template_name = "approvals.html"
    list = []
    tracklist = []

    def get(self, request, *args, **kwargs):
        '''if GET  '''
        if request.user.is_authenticated:
            permissions = Permission.objects.filter(user = request.user)
            for permission in permissions:
                results = Resident.objects.filter(tracking_status = True,facility_name =permission.codename)
                self.list = list()

                for result in results:
                    self.list.append(result)
                return render(request,self.template_name, {'list':self.list,"form":self.form_class})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):

        pass

class NotTrackingView(View):
    form_class = ApplicationForm
    template_name = "not_tracking.html"
    list = []
    tracklist = []

    def get(self, request, *args, **kwargs):
        '''if GET  '''

        results = Resident.objects.filter(tracking_status = False)
        self.list = list()

        for result in results:
            self.list.append(result)

        return render(request,self.template_name, {'list':self.list,"form":self.form_class})

    def post(self, request, *args, **kwargs):
        pass
