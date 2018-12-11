from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ApplicationForm, UploadFileForm
from application.models import Facility,Resident, ApplicationTracking, Alert
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
        payor_change_results = Resident.objects.filter(tracking_status = None, activity_type = 'P')
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

        alerts = Alert.objects.filter(alert_status = False)
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

        self.list = list()

        for result in results:
            alert = result

        resident = Resident.objects.get(resident_id = resident_id)

        results = ApplicationTracking.objects.filter(resident = resident)



        for result in results:
            application = result
    
        return render(request,self.template_name, {'alert':alert,'application':application,"form":self.form_class})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        file = request.FILES.getlist('files')[0]
        type = request.POST.get('file_type')
        resident_id = request.POST.get('resident_id')


        tracking = ApplicationTracking.objects.get(resident_id = resident_id)
        field = getattr(tracking, type)
        # TODO
        field.save(str(resident_id),file)
        tracking.save()
        return HttpResponse("200")
        # self.list = list()
        # for result in results:
        #     facility = result.Facility
        #
        #     self.list.append(al.get_fields(result, facility))
        #
        # return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})


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
