from django import forms


class loginForm(forms.Form):
    userName = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)