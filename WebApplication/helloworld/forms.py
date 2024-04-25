from django import forms
from django.contrib.auth.models import User

class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
    class Meta:
        model = User



class bookingForm(forms.Form):
    accountID = forms.CharField(label = "accountID",max_length = 30)
    itemID = forms.CharField(label = "ID",max_length = 30)
    startDate = forms.CharField(label = "Start Date",max_length = 30)
    endDate = forms.CharField(label = "End Date",max_length = 30)
    bookingStatus = forms.CharField(label = "Status",max_length = 30) # this will just be true, admin will not have to accept these
    class Meta:
        fields = ['accountID','itemID','startDate','endDate','bookingStatus']
        