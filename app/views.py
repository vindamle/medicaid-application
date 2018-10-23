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
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        return render(request,self.template_name, {"form":self.form_class, 'facilities':facilities})

    def post(self, request, *args, **kwargs):
        facilities =Facility.objects.filter(downstate_upstate__isnull = False )
        print(request.POST.get('Facility'))

        print(int(request.POST.get("days")))

        al = Alerts()
        results = al.get_alerts(3, "N. Manor")
        self.list = list()
        for result in results:
            facility = result.Facility
            self.list.append(al.get_fields(result, facility))

        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class, 'facilities':facilities, "tracklist":self.tracklist})
