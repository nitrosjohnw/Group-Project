from django.shortcuts import render
from django.http import HttpResponse
from .forms import loginForm
# Create your views here.
def home(request):

    return render(request,"home.html")

def account(request):

    return render(request,"account.html")

def bookingPage(request):

    return render(request,"booking.html")

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = loginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request,"login.html", {"status": "Success"})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()

    return render(request,"login.html")