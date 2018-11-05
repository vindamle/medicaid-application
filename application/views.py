from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import NameForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Alert

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
        requested_patient_id = request.GET['patient_id']
        track = request.GET['tracking']
        requested_patient_id = int(requested_patient_id)
        alert = Alert.objects.get(patient_id = requested_patient_id)
        if track == "true":
            alert.tracking_status = True
            alert.save()
        elif track == "false":
            alert.tracking_status = False
            alert.save()
        return HttpResponse("200") # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")
