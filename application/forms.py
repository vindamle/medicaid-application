from django import forms
import datetime
class NameForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    ncs_id_number = forms.CharField()
    medicaid_application = forms.FileField()
    confirmation_reciept = forms.FileField()
    RFI = forms.FileField()
    RFI_deadline = forms.DateField(initial=datetime.date.today)




class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
