from django.shortcuts import render
from django.contrib.auth import authenticate, login
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
        username = request.POST["username"]
        password = request.POST["password"]
        # create a form instance and populate it with data from the request:
        form = loginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
        # Redirect to a success page.
                return render(request,"login.html", {"status": "Success"})
            else:
        # Return an 'invalid login' error message.
        
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
                return render(request,"login.html", {"status": "Failed"})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()

    return render(request,"login.html")