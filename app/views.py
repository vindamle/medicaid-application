from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .forms import ApplicationForm, UploadFileForm
from application.models import *
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
from django.contrib import messages
from django.http import JsonResponse


from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Permission

class LoginView(View):
    template_name = "registration/login.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):

        login_data = authenticate(username = request.POST.get("username"), password = request.POST.get("password"))

        if login_data:
            request.session.set_expiry(0)
            login(request, login_data)
            return redirect('home')

        messages.error(request, 'Oops! Wrong username or password. Please try again.')
        return redirect('login')



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
                    print("*" * 50)
                    print(app.resident.first_name)
                    applications.append(app)

            return render(request,self.template_name, {'applications':applications})
        else:
            return redirect('login')


# ActivityView
# Shows Lists of all residents that have not been tracked or untracked
class ActivityView(View):

    template_name = "activity.html"

    #Returns Residents with new activities that have not been tracked/not tracked
    def get(self, request, *args, **kwargs):

        new_admission = []
        payor_change = []
        discharge = []

        if request.user.is_authenticated:
            permissions = Permission.objects.filter(user = request.user)

            for permission in permissions:

                new_admits = Resident.objects.filter(facility_name =permission.codename, tracking_status = None, activity_type = 'A')
                for new_admit in new_admits:
                    new_admission.append(new_admit)

                new_payor_changes = Resident.objects.filter(facility_name =permission.codename,activity_type = 'P', dismiss = False)
                for new_payor_change in new_payor_changes:
                    payor_change.append(new_payor_change)

                new_discharges= Resident.objects.filter(facility_name =permission.codename,tracking_status = None, activity_type = 'D')
                for new_discharge in new_discharges:
                    discharge.append(new_discharge)

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

            self.list = list()
            for permission in permissions:

                residents = Resident.objects.filter(facility_name =permission.codename, tracking_status = True)


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
        misc_docs = Document.objects.filter(resident_id = resident_id, description = 'misc_doc').order_by('application_id')
        denials = Denial.objects.filter(response__application__resident__resident_id = resident_id).order_by('response__application__application_id','denial_id')
        approvals = Approval.objects.filter(response__application__resident__resident_id = resident_id).order_by('response__application__application_id','approval_id')
        namis = NAMI.objects.filter(approval__response__application__resident__resident_id = resident_id).order_by('approval__approval_id', 'nami_id')
        fair_hearings = FairHearing.objects.filter(response__application__resident__resident_id = resident_id).order_by('response__response_id', 'fair_hearing_id')
        # medicaid_application_documents = Document.objects.filter(resident_id = resident_id, description = "medicaid_application")
        # rfi_documents = Document.objects.filter(resident_id = resident_id, description = "rfi").order_by('rfi_id')
        # applications = results
        # print('*'*50)
        # print(denials)
        # print('*'*50)
        # return render(request,self.template_name, {'rfis':rfis,'documents':documents,'resident':resident,'applications':applications,"resident_alerts":resident_alerts, 'medicaid_application_documents': medicaid_application_documents, "rfi_documents":rfi_documents, "form":self.form_class})
        return render(request, self.template_name, {'resident': resident, 'applications':applications, 'rfis':rfis, 'denials': denials, 'approvals': approvals, 'namis': namis, 'fair_hearings': fair_hearings, 'resident_alerts': resident_alerts, 'misc_docs': misc_docs})
    def post(self, request, *args, **kwargs):

        file = request.FILES.getlist('file')
        type = request.POST.get('file_type')
        resident_id = request.POST.get('resident_id')
        application_id = request.POST.get('application_id')
        row_id = request.POST.get('row_id')
        ROOT = Path.cwd()
        path = Path(str(ROOT) + "/static/applications/"+resident_id+"/"+str(application_id))
        if not path.exists():
            path.mkdir(parents=True, exist_ok = True)

        try:
            new_document = Document.objects.create(
                resident = Resident.objects.get(resident_id = resident_id),
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
            snowden_update(request,application, application.application_id,"application_document_id",new_document.document_id)
            application.application_document = new_document
            application.save()
        elif type == 'rfi':
            rfi = RFI.objects.get(rfi_id = int(request.POST.get('row_id')))
            snowden_update(request,rfi, rfi.rfi_id,"document_id",new_document.document_id)
            rfi.document_id = new_document.document_id
            rfi.save()
        elif type == 'approval':
            approval = Approval.objects.get(approval_id = int(request.POST.get('row_id')))
            snowden_update(request,approval, approval.approval_id,"document_id",new_document.document_id)
            approval.document_id = new_document.document_id
            approval.save()
        elif type == 'denial':
            denial = Denial.objects.get(denial_id = int(request.POST.get('row_id')))
            snowden_update(request,denial, denial.denial_id,"document_id",new_document.document_id)
            denial.document_id = new_document.document_id
            denial.save()
        elif type == 'application_confirmation':
            confirmation = Confirmation.objects.create(confirmation_document = new_document, description = type)
            snowden_update(request,confirmation, confirmation.confirmation_id,"confirmation_document_id",confirmation.confirmation_document_id)
            application = Application.objects.get(application_id = int(application_id))
            snowden_update(request,application, application.application_id,"application_confirmation_id",confirmation.confirmation_id)
            application.application_confirmation = confirmation
            application.save()

        elif type == "fair_hearing_confirmation":
            confirmation = Confirmation.objects.create(confirmation_document = new_document, description = type)
            snowden_update(request,confirmation, confirmation.confirmation_id,"confirmation_document_id",confirmation.confirmation_document_id)
            fair_hearing = FairHearing.objects.get(fair_hearing_id = int(row_id))
            snowden_update(request,fair_hearing, fair_hearing.fair_hearing_id,"fair_hearing_confirmation_id",confirmation.confirmation_id)
            fair_hearing.fair_hearing_confirmation = confirmation
            fair_hearing.save()

        elif type == "fair_hearing_outcome_document":
            fair_hearing = FairHearing.objects.get(fair_hearing_id = int(row_id))
            snowden_update(request,fair_hearing, fair_hearing.fair_hearing_id,"fair_hearing_outcome_document_id",new_document.document_id)
            fair_hearing.fair_hearing_outcome_document_id = new_document.document_id
            fair_hearing.save()


        # return redirect('/show/?resident_id={}'.format(str(resident_id)))
        # return HttpResponse(new_document.file_name)
        return JsonResponse([str(new_document.file), new_document.file_name, new_document.document_id, new_document.date_uploaded], safe=False)

def snowden_update(request,table_name, row_id, column, new_value):
    # Audit Log
    Snowden.objects.create(
        user = request.user,
        table_name = table_name._meta.verbose_name,
        row_id = row_id,
        column_name = column,
        old_value = getattr(table_name,column) if getattr(table_name,column) is not None else "None",
        new_value = new_value,
        log_ip = request.META.get('REMOTE_ADDR'),
        date = datetime.now()
    )

class ApprovalsView(View):
    form_class = ApplicationForm
    template_name = "approvals.html"
    list = []
    tracklist = []

    def get(self, request, *args, **kwargs):
        self.list = []
        if request.user.is_authenticated:
            permissions = Permission.objects.filter(user = request.user)
            for permission in permissions:
                results = Application.objects.filter(tracking_status = True,resident__facility_name =permission.codename)


                for result in results:
                    self.list.append(result)

            return render(request,self.template_name, {'applications':self.list,"form":self.form_class})
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
