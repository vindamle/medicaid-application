from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .forms import ApplicationForm, UploadFileForm
from application.models import Facility,Resident, ApplicationTracking, Alert, Document
import pandas as pd


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
        payor_change_results = Resident.objects.filter(activity_type = 'P')
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
        for resident in residents:
            alerts = Alert.objects.filter(resident = resident , alert_status = False)
            self.list = list()

            for alert in alerts:
                print(alert.resident.resident_id)
                self.list.append(alert)
        print(self.list)
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
        results = Resident.objects.filter(resident_id = resident_id)

        for result in results:
            alert = result

        resident = Resident.objects.get(resident_id = resident_id)
        results = ApplicationTracking.objects.filter(resident = resident)

        for result in results:
            application_alerts = result
        resident_alert = Alert.objects.filter(resident_id = resident_id, application_id = application_alerts.tracking_id)


        application = results

        return render(request,self.template_name, {'alert':alert,'application':application,"resident_alert":resident_alert,"form":self.form_class})

    def post(self, request, *args, **kwargs):


        file = request.FILES.getlist('files')
        type = request.POST.get('file_type')
        resident_id = request.POST.get('resident_id')
        print(file, type, int(resident_id))

        application_id = request.POST.get('application_id')

        resident = Resident.objects.get(resident_id = resident_id)
        application = ApplicationTracking.objects.get(tracking_id = application_id)

        Document.objects.create(
            resident =resident,
            application = application,
            file = file,
            description = type,
            date_recieved = datetime.now(),
        )

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
