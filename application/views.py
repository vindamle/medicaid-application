from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import NameForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Resident, ApplicationTracking, Alert, AlertType
from .additionalInfo import AdditionalInfo

class signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class create(generic.CreateView):
    form_class = NameForm
    success_url = reverse_lazy('home')
    template_name = 'create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})

def update_list(request):
    if request.method == 'GET':
        requested_resident_id = request.GET['resident_id']
        track = request.GET['tracking']
        requested_resident_id = int(requested_resident_id)
        alert = Resident.objects.get(resident_id = requested_resident_id)
        alert_type = AlertType.objects.get(alert_type_id = 1)
        if track == "true":
            alert.tracking_status = True


            Alert.objects.create(
                resident =alert,
                application = None,
                alert_priority = 1,
                alert_message = "Application Not Started",
                alert_type = alert_type,
            )
            alert.save()


            # resident_info = AdditionalInfo()


        elif track == "false":
            alert.tracking_status = False
            alert.save()
        return HttpResponse("200") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")

def approval_verified(request):
    if request.method == 'GET':
        resident_id =int(request.GET['resident_id'])

        application = ApplicationTracking.objects.get(resident = resident_id)
        print(application)
        if request.GET['approval_verified'] == "True":
            application.approval_verified = True
            application.save()
        else:
            application.approval_verified = False
            application.save()

        return HttpResponse("200")
    else:
        return HttpResponse("Request method is not a GET")


def update_resident(request):
    return HttpResponse("200")

def update_application(request):
    return HttpResponse("200")

def update_alerts(request):
    return HttpResponse("200")
