from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from helloworld.forms import loginForm
from helloworld.forms import signUpForm
# Create your views here.

def UserLoggedIn(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


def GetUserName(request):
    return request.user.username
    


def home(request):

    return render(request,"home.html")

def account(request):

    return render(request,"account.html")

def bookingPage(request):

    return render(request,"booking.html")

def signUp(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        # create a form instance and populate it with data from the request:
        form = signUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                context = {
                'form':form,
                'user':user
                }
        # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {
                'form':form
                }
                return render(request,"signup.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = signUpForm()
        context = {
        'form':form
        }

        return render(request,"signup.html",context) 
    return render(request,"signup.html")

def loginPage(request):
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
                login(request,user)
                context = {
                'form':form,
                'user':user
                }
        # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {
                'form':form
                }
                return render(request,"login.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()
        context = {
        'form':form
        }

        return render(request,"login.html",context) 
    

def accountPage(request):
    return render(request,"account.html")

def userLogout(request):
        logout(request)
        return render(request,"home.html")