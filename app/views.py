from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .forms import ApplicationForm

class HomeView(View):
    form_class = ApplicationForm
    template_name = "home.html"
    list = []

    def get(self, request, *args, **kwargs):

        self.list = [
            {"id":1, "first_name":"John", "last_name":"Smith","type": "Certificate Exprired", "date":"10/1/2018"},
            {"id":2, "first_name":"Jane", "last_name":"Doe","type": "Application Denied", "date":"10/15/2018"},
            {"id":1, "first_name":"John", "last_name":"Smith","type": "Certificate Exprired", "date":"10/1/2018"},
            {"id":2, "first_name":"Jane", "last_name":"Doe","type": "Application Denied", "date":"10/15/2018"},
            {"id":1, "first_name":"John", "last_name":"Smith","type": "Certificate Exprired", "date":"10/1/2018"},
            {"id":2, "first_name":"Jane", "last_name":"Doe","type": "Application Denied", "date":"10/15/2018"},
            {"id":2, "first_name":"Jane", "last_name":"Doe","type": "Application Denied", "date":"10/15/2018"},
            {"id":1, "first_name":"John", "last_name":"Smith","type": "Certificate Exprired", "date":"10/1/2018"},
        ]
        return render(request,self.template_name, {'list':self.list, "alert_length":len(self.list) , "form":self.form_class})
