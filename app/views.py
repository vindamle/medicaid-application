from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ApplicationForm
from application.models import Facility,Alert
from application.alerts import Alerts


class HomeView(View):
    form_class = ApplicationForm
    template_name = "home.html"
    list = []
    tracklist = []


    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Alert.objects.filter(tracking_status = True)
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
        results = Alert.objects.filter(tracking_status = None)
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


class PendingView(View):
    form_class = ApplicationForm
    template_name = "pending_alerts.html"
    list = []
    tracklist = []


    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Alert.objects.filter(tracking_status = None)
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


class ShowView(View):
    form_class = ApplicationForm
    template_name = "show.html"
    list = []
    tracklist = []



    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Alert.objects.filter(tracking_status = None)
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


class ApprovalsView(View):
    form_class = ApplicationForm
    template_name = "approvals.html"
    list = []
    tracklist = []



    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        results = Alert.objects.filter(tracking_status = None)
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
        results = Alert.objects.filter(tracking_status = False)
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
