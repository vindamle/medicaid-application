from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .forms import ApplicationForm, UploadFileForm
from application.models import Facility,Resident, ApplicationTracking, Alert, Document, RFI
import pandas as pd
from datetime import datetime
import os
from pathlib import Path


class HomeView(View):
    form_class = ApplicationForm
    template_name = "home.html"
    list = []
    tracklist = []

    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Resident.objects.filter(tracking_status = True)
        self.list = list()

        for result in results:
            self.list.append(result)

        return render(request,self.template_name, {'list':self.list,"form":self.form_class, 'facilities':facilities})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )

        self.list = list()
        for result in results:
            facility = result.Facility

            self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})


class ActivityView(View):
    form_class = ApplicationForm
    template_name = "activity.html"
    list = []
    tracklist = []



    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        new_admission_results = Resident.objects.filter(tracking_status = None, activity_type = 'A')

        payor_change_results = Resident.objects.filter(activity_type = 'P', dismiss = False)
        discharge_results = Resident.objects.filter(tracking_status = None, activity_type = 'D')
        self.payor_change_list = []
        self.new_admission_list = []
        self.discharge_list = []

        for result in payor_change_results:
            self.payor_change_list.append(result)
        for result in new_admission_results:
            self.new_admission_list.append(result)
        for result in discharge_results:
            self.discharge_list.append(result)

        return render(request,self.template_name, {'discharge':self.discharge_list,'list':self.new_admission_list,'payor_change':self.payor_change_list,"form":self.form_class, 'facilities':facilities})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )


        self.list = list()
        for result in results:
            facility = result.Facility

            self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})


class PendingView(View):
    form_class = ApplicationForm
    template_name = "pending_alerts.html"
    list = []
    tracklist = []


    def get(self, request, *args, **kwargs):
        '''if GET  '''
        residents = Resident.objects.filter(tracking_status = True)
        self.list = list()
        for resident in residents:

            alerts = Alert.objects.filter(resident = resident , alert_status = False)

            for alert in alerts:
                self.list.append(alert)

        return render(request,self.template_name, {'list':self.list,"form":self.form_class})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )


        self.list = list()
        for result in results:
            facility = result.Facility

            self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})


class ShowView(View):
    form_class = UploadFileForm
    template_name = "show.html"
    list = []
    tracklist = []



    def get(self, request, *args, **kwargs):
        '''if GET  '''

        resident_id= int(request.GET["resident_id"])
        resident = Resident.objects.get(resident_id = resident_id)
        results = ApplicationTracking.objects.filter(resident = resident)

        for result in results:
            application_alerts = result

        resident_alerts = Alert.objects.filter(resident_id = resident_id, application_id = application_alerts.tracking_id, alert_status = False)

        documents = Document.objects.filter(resident_id = resident_id)
        rfis = RFI.objects.filter(resident_id = resident_id)
        medicaid_application_documents = Document.objects.filter(resident_id = resident_id, description = "medicaid_application")
        rfi_documents = Document.objects.filter(resident_id = resident_id, description = "rfi").order_by('date_recieved')
        applications = results
        # print(application)
        return render(request,self.template_name, {'rfis':rfis,'documents':documents,'resident':resident,'applications':applications,"resident_alerts":resident_alerts, 'medicaid_application_documents': medicaid_application_documents, "rfi_documents":rfi_documents, "form":self.form_class})

    def post(self, request, *args, **kwargs):


        file = request.FILES.getlist('document')
        type = request.POST.get('file_type')
        resident_id = request.POST.get('resident_id')
        application_id = request.POST.get('application_id')

        resident = Resident.objects.get(resident_id = int(resident_id))
        application = ApplicationTracking.objects.get(tracking_id = application_id)

        
        ROOT = Path.cwd()
        path = Path(str(ROOT) + "/static/applications/"+str(resident_id)+"/"+str(application_id))
        if not path.exists():
            print("Create Path")
            path.mkdir(parents=True, exist_ok = True)

        # if type == 'rfi':
        #     rfi = RFI.objects.get(rfi_id = int(request.POST.get('rfi_id')))


        try:
            x = Document.objects.create(
                resident =resident,
                application = application,
                file = file[0],
                file_name = (file[0].name).split(".")[0],
                description = type,
                date_recieved = datetime.now(),
                rfi_id = int(request.POST.get('rfi_id')) if type == 'rfi' else None
            )
        except Exception as e:
            print("\n\n",str(e),"\n\n")

        if type == 'rfi':
            rfi = RFI.objects.get(rfi_id = int(request.POST.get('rfi_id')))
            rfi.document_id = x.document_id
            rfi.save()

        return redirect('/show/?resident_id={}'.format(request.POST.get('resident_id')))



class ApprovalsView(View):
    form_class = ApplicationForm
    template_name = "approvals.html"
    list = []
    tracklist = []

    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Resident.objects.filter(tracking_status = True)
        self.list = list()

        for result in results:
            self.list.append(result)
        return render(request,self.template_name, {'list':self.list,"form":self.form_class, 'facilities':facilities})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )


        self.list = list()
        for result in results:
            facility = result.Facility

            self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})

class NotTrackingView(View):
    form_class = ApplicationForm
    template_name = "not_tracking.html"
    list = []
    tracklist = []

    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Resident.objects.filter(tracking_status = False)
        self.list = list()

        for result in results:
            self.list.append(result)

        return render(request,self.template_name, {'list':self.list,"form":self.form_class, 'facilities':facilities})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )


        self.list = list()
        for result in results:
            facility = result.Facility

            self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})
