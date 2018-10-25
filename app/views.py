from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ApplicationForm
from application.models import Facility
from application.alerts import Alerts


class HomeView(View):
    form_class = ApplicationForm
    template_name = "home.html"
    list = []
    tracklist = []


    def get(self, request, *args, **kwargs):
        '''if GET  '''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        return render(request,self.template_name, {"form":self.form_class, 'facilities':facilities})

    def post(self, request, *args, **kwargs):

        '''if POST'''
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )

        al = Alerts()
        results = al.get_alerts(10, "All")
        self.list = list()
        for result in results:
            facility = result.Facility
            print(result)
            # self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})
