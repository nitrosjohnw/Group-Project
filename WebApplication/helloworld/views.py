from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from helloworld.forms import loginForm, bookingForm ,signUpForm
from django.contrib.auth.models import User
from helloworld.models import Equipment, Booking
# Create your views here.

def UserLoggedIn(request): #uop
    if request.user.is_authenticated:
        return True
    else:
        return False

def getUserBookings(request):
    return Booking.objects.filter(account = request.user)


def GetUserName(request):
    return request.user.username
    

def getEquipmentBetweenDate(startDate, endDate):
    #look at length of booing table that is returned when filtered then take that away from equipment available
    bookings = Booking.objects.all()
    equipment = Equipment.objects.all()
    for booking in bookings:
        if booking.startDate >= startDate and booking.endDate <= endDate:
            for equipment in equipment:
                if equipment.equipmentID == booking.equipmentID:
                    equipment.equipmentQuantity = equipment.equipmentQuantity - 1
    
    
    for i in equipment:
        if i.equipmentQuantity >= 0:
            equipment = equipment.exclude(equipmentID = i.equipmentID)
    
    #return the equipment that is available
    return equipment

def authBooking(bookingDetails):
    canBook = True
    if Equipment.objects.filter(equipmentID = bookingDetails['itemID']).exists() and User.objects.filter(id = bookingDetails['accountID']).exists():
        if Booking.objects.filter(startDate = bookingDetails['itemID']).exists:
            for i in Booking.objects.filter(equipmentID = bookingDetails['itemID']):
                # write a if statement to check if the dates are available
                if bookingDetails['startDate'] >= i.startDate and bookingDetails['startDate'] <= i.endDate:
                    canBook = False
        else:
            canBook = False
        return canBook
    else:
        return False


def home(request):

    return render(request,"home.html")



def bookingPage(request):

    return render(request,"booking.html")

def signUp(request):
    print(request.POST)
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        
        if User.objects.filter(email=email).exists():
            context = {
                'form': signUpForm(),
                'status': 'Email already in use'
            }
            return render(request, "signup.html", context)
         # create a form instance and populate it with data from the request:
        form = signUpForm(request.POST)
        # check whether it's valid:
        if (not(password == password2)):
            context = {
            'form':form,
            'status':'Passwords do not match'
            }
            return render(request,"signup.html",context)
       
        if form.is_valid():
            try: 
                user = User.objects.create(username = username, email = email,) 
                user.first_name = fname
                user.last_name = lname
                user.set_password(password)
                user.save()
            except:
                context = {
                'form':form,
                'status':'Username already exists'
                }
                return render(request,"signup.html", context)
            
            if user is not None:
                login(request,user)
                context = {
                'form':form,
                'user':user,
                'status':'Sign Up Successful'
                }
                # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {
                'form':form,
                'status':'Signup Failed'
                }
                return render(request,"signup.html", context)

    # if a GET (or any other method) we'll create a blank form
        else:
            form = signUpForm()
            context = {
            'form':form,
            'status':'Invalid Username or Password',
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
        if request.user.is_authenticated:
            context = {
            'form':form,
            'status':'Already Logged In'
            }
            return render(request,"home.html",context)
       
        if form.is_valid():
            print("Form is Valid")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("User is not None")
                login(request,user)
                context = {
                'form':form,
                'user':user,
                'status':'Login Successful',
                }
        # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {
                'form':form,
                'status':'Invalid Username or Password'
                }
                return render(request,"login.html", context)
        else:
            print("Form is Invalid")
            context = {
            'form':form,
            'status':'Invalid Username or Password'
            }
            return render(request,"login.html", context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()
        context = {
        'form':form,
        'status':'',
        }
        return render(request,"login.html",context) 
    


def userLogout(request):
        logout(request)
        request.user = None
        return render(request,"home.html")

def account(request):
    print("here")
    if UserLoggedIn(request):
        print("User is Logged In")
        usersBookings = getUserBookings(request)
        context = {
        'username':GetUserName(request),
        'bookings':usersBookings
        }

        return render(request,"account.html",context)
    else:
        return loginPage(request)

def bookingPage(request):
    equipment = Equipment.objects.all()
    if not UserLoggedIn(request):
        return loginPage(request)
    
    usersBookings = getUserBookings(request)
    if request.method == "POST":
        print(request.POST)
        form = bookingForm(request.POST)
        if form.is_valid():
            #accountID = request.POST["accountID"]
            user = request.user
            accountID = user.id
            itemID = request.POST["itemID"]
            startDate = request.POST["startDate"]
            endDate = request.POST["endDate"]
            
            bookingStatus = True
            context = {
                'bookings':usersBookings,
                'equipment':equipment,
                'accountID':accountID,
                'itemID':itemID,
                'startDate':startDate,
                'endDate':endDate,
                'bookingStatus':bookingStatus
            }
            context['bookingStatus'] = True #authBooking(context)
            print(context['bookingStatus'])
            if context['bookingStatus'] == True:
                user = User.objects.filter(id = user.id).first()
                item = Equipment.objects.filter(equipmentID = itemID).first()
                print(item)
                booking = Booking.create(startDate, endDate, "O", user,item)
                booking.save()
                print("Booking Successful")
                return render(request,"booking.html",context)
    form = bookingForm()
    context = {
        'bookings':usersBookings, 
        'equipment':equipment,
        'accountID':1,
        'itemID':1,
        'startDate':1,
        'endDate':1,
        'bookingStatus':False
    }
    return render(request,"booking.html", context)