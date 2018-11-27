from django import forms
import datetime

class ApplicationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    facility = forms.CharField()
    admission_date = forms.DateField()
    pick_up_date =  forms.CharField()
    application_type =  forms.DateField()
    medicaid_application = forms.FileField()
    confirmation_reciept = forms.FileField()
    RFI = forms.FileField()
    RFI_issue_date = forms.DateField(initial=datetime.date.today)
    RFI_deadline = forms.DateField()




class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
