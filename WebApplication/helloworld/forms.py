from django import forms
from django.contrib.auth.models import User
from .models import Booking
class loginForm(forms.Form):
    # Form fields for logging in
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)

    class Meta:
        model = User

class signUpForm(forms.Form):
    # Form fields for signing up
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
    password2 = forms.CharField(label="Password2", max_length=50)
    email = forms.EmailField(label="Email")
    fname = forms.CharField(label="fname", max_length=70)
    lname = forms.CharField(label="lName", max_length=70)

    class Meta:
        model = User

class bookingSort(forms.Form):
    # Form fields for sorting bookings
    startDate = forms.DateField(label="Start Date")
    endDate = forms.DateField(label="End Date")

    class Meta:
        fields = ['startDate', 'endDate']

class bookingForm(forms.Form):
    # Form fields for booking equipment
    itemID = forms.IntegerField(label="ID")
    startDate = forms.DateField(label="Start Date")
    endDate = forms.DateField(label="End Date")

    class Meta:
        model = Booking
        fields = ['itemID', 'startDate', 'endDate']

class changePasswordForm(forms.Form):
    # Form fields for changing password
    currentPassword = forms.CharField(label="Current Password", max_length=50)
    password = forms.CharField(label="New Password", max_length=50)
    password2 = forms.CharField(label="New Password2", max_length=50)

    class Meta:
        model = User