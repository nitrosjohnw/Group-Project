from django import forms
from django.contrib.auth.models import User
from .models import Booking
class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
    class Meta:
        model = User

class signUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
    password2 = forms.CharField(label="Password2", max_length=50)
    email = forms.EmailField(label="Email")
    fname = forms.CharField(label="fname", max_length=70)
    lname = forms.CharField(label="lName", max_length=70)
    class Meta:
        model = User

class bookingSort(forms.Form):
    #accountID = forms.CharField(label = "accountID",max_length = 30)
    startDate = forms.DateField(label = "Start Date")
    endDate = forms.DateField(label = "End Date")
    #bookingStatus = forms.CharField(label = "Status",max_length = 30) # this will just be true, admin will not have to accept these
    class Meta:
        fields = ['startDate','endDate']

class bookingForm(forms.Form):
    #accountID = forms.CharField(label = "accountID",max_length = 30)
    itemID = forms.IntegerField(label = "ID")
    startDate = forms.DateField(label = "Start Date")
    endDate = forms.DateField(label = "End Date")
    #bookingStatus = forms.CharField(label = "Status",max_length = 30) # this will just be true, admin will not have to accept these
    class Meta:
        model = Booking
        fields = ['itemID','startDate','endDate']


class changePasswordForm(forms.Form):
    currentPassword = forms.CharField(label="Current Password", max_length=50)
    password = forms.CharField(label="New Password", max_length=50)
    password2 = forms.CharField(label="New Password2", max_length=50)
    class Meta:
        model = User