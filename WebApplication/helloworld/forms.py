from django import forms
from django.contrib.auth.models import User


class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
    class Meta:
        model = User