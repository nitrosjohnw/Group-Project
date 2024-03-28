from django.shortcuts import render

# Create your views here.
def home(request):

    return render(request,"home.html")

def account(request):

    return render(request,"account.html")

def bookingPage(request):

    return render(request,"booking.html")

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

        # Return an 'invalid login' error message.
        
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
                return render(request,"login.html", {"status": "Failed"})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()
        context = {
        'form':form
        }

        return render(request,"login.html",context) 