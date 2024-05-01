from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from helloworld.forms import loginForm, bookingForm ,signUpForm, changePasswordForm
from django.contrib.auth.models import User
from helloworld.models import Equipment, Booking
import datetime
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
    
def doDatesOverlap(start_date_a, end_date_a, start_date_b, end_date_b):
    # Check if end_date_a is before or equal to start_date_b or start_date_a is after or equal to end_date_b
    if end_date_a <= start_date_b or start_date_a >= end_date_b:
        return False
    else:
        return True
    

def getEquipmentBetweenDate(startDate, endDate):
    #look at length of booing table that is returned when filtered then take that away from equipment available
    bookings = Booking.objects.all()
    equipment = Equipment.objects.all()

    for booking in bookings:
        if (doDatesOverlap(startDate, endDate, booking.startDate, booking.endDate)):
            for item in range(len(equipment)):
                if equipment[item] == booking.equipment:

                    equipment[item].equipmentQuantity = equipment[item].equipmentQuantity - 1
    
    items = len(equipment)
    newEquipment = []
    for item in range(items):

        if equipment[item].equipmentQuantity <= 0:
            continue
        newEquipment.append(equipment[item])
    
    equipment = newEquipment
    
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


def signUp(request):

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
                user = User.objects.create(username = username, email = email, first_name = fname, last_name = lname) 
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
        else:
            form = signUpForm()
            context = {
            'form':form,
            'status':'Invalid Username or Details',
            } 
            return render(request,"signup.html",context)
    # if a GET (or any other method) we'll create a blank form
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
            'status':'Already Logged In',
            'user': request.user,
            }
            return render(request,"home.html",context)

        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
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
    
def support(request):
    if not UserLoggedIn(request):
        return loginPage(request)
    
    usersBookings = getUserBookings(request)
    context = {
        'username':GetUserName(request),
        'bookings':usersBookings
        }
    return render(request,"support.html",context)

def userLogout(request):
        logout(request)
        
        request.user = None
        return loginPage(request)

def changePassword(request):
    if UserLoggedIn:
        if request.method == "POST":
            user = request.user
            oldPassword = request.POST["currentPassword"]
            password = request.POST["password"]
            password2 = request.POST["password2"]
            form = changePasswordForm(request.POST)
            print(form)
            if form.is_valid():
                
                if not(user.check_password(oldPassword)):
                    context = {
                    'username':GetUserName(request),
                    'status':'Incorrect Password'
                    }
                    return render(request,"account.html",context)
                
                if (not(password == password2)):
                    context = {
                    'username':GetUserName(request),
                    'status':'Passwords do not match'
                    }
                    return render(request,"account.html",context)
                
                user.set_password(password)
                user.save()
                context = {
                    'username':GetUserName(request),
                    'status':'Password Changed'
                }
                return render(request,"account.html",context)
            else:
                context = {
                    'username':GetUserName(request),
                    'status':'Invalid Password'
                }
                return render(request,"account.html",context)
            
    else:
        return loginPage(request)

def account(request):
    if UserLoggedIn(request):
        usersBookings = getUserBookings(request)
        context = {
        'username':GetUserName(request),
        'email':request.user.email,
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'bookings':usersBookings
        }

        return render(request,"account.html",context)
    else:
        return loginPage(request)


def cancelBooking(request):

    if UserLoggedIn(request):
        if request.method == "POST":
            bookingID = request.POST["bookingID"]
            print(bookingID)
            booking = Booking.objects.filter(bookingID = bookingID).first()
            
            if booking.account != request.user:
                context = {
                    'username':GetUserName(request),
                    'email':request.user.email,
                    'first_name':request.user.first_name,
                    'last_name':request.user.last_name,
                    'bookings':getUserBookings(request),
                    'status':'You cannot cancel this booking'
                }
                return render(request,"account.html",context)
            booking.delete()
            context = {
                'username':GetUserName(request),
                'email':request.user.email,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'bookings':getUserBookings(request),
                'status':'Booking Cancelled'
            }
            return render(request,"account.html",context)
        else:
            context = {
                'username':GetUserName(request),
                'email':request.user.email,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'bookings':getUserBookings(request),
                'status':''
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
        #if the user wants to sort the equipment
        if request.POST["Sort"] == "Sort":
            try:
                startDate = request.POST["startDate"]
                endDate = request.POST["endDate"]
                startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
                endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
            except:
                user = request.user
                accountID = user.id
                context = {
                'bookings':usersBookings,
                'equipment':equipment,
                'accountID':accountID,
                'itemID':1,
                'startDate':1,
                'endDate':1,
                'bookingStatus':False
                }
                return render(request,"booking.html",context)

            equipment = getEquipmentBetweenDate(startDate, endDate)
            context = {
                'bookings':usersBookings,
                'equipment':equipment,
                'accountID':1,
                'itemID':1,
                'startDate':startDate,
                'endDate':endDate,
                'bookingStatus':False
            }
            return render(request,"booking.html",context)
        
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
            if context['bookingStatus'] == True:
                user = User.objects.filter(id = user.id).first()
                item = Equipment.objects.filter(equipmentID = itemID).first()
                booking = Booking.create(startDate, endDate, "O", user,item)
                booking.save()
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