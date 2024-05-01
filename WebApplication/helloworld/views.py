from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from helloworld.forms import loginForm, bookingForm ,signUpForm, changePasswordForm
from django.contrib.auth.models import User
from helloworld.models import Equipment, Booking
import datetime
# Create your views here.

#Edited by Toby, Mathew, Lucian, David and John


#Toby
def UserLoggedIn(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

#Toby
def getUserBookings(request):
    return Booking.objects.filter(account = request.user)

#Toby
def GetUserName(request):
    return request.user.username

#Toby
def doDatesOverlap(start_date_a, end_date_a, start_date_b, end_date_b):
    # Check if end_date_a is before or equal to start_date_b or start_date_a is after or equal to end_date_b
    if end_date_a <= start_date_b or start_date_a >= end_date_b:
        return False
    else:
        return True

#Toby
def getEquipmentBetweenDate(startDate, endDate):
    #look at length of booing table that is returned when filtered then take that away from equipment available
    bookings = Booking.objects.all()
    equipment = Equipment.objects.all()

    for booking in bookings: #loop through all bookings
        if (doDatesOverlap(startDate, endDate, booking.startDate, booking.endDate)):#if the dates overlap then remove the equipment from the list
            for item in range(len(equipment)): #loop through equipment
                if equipment[item] == booking.equipment: #if the equipment take one away

                    equipment[item].equipmentQuantity = equipment[item].equipmentQuantity - 1 #take away quantity of equipment
    
    items = len(equipment)
    newEquipment = []
    for item in range(items): #loop through equipment

        if equipment[item].equipmentQuantity <= 0: #if the equipment quantity is 0 or less than 0 then skip this equipment
            continue
        newEquipment.append(equipment[item]) #add the equipment to the new list
    
    equipment = newEquipment #set the equipment to the new list
    
    #return the equipment that is available
    return equipment

#Davod
def TC(request):
    return render(request,"Terms&Conditions.html")

def home(request):

    return render(request,"home.html")


 #Matthew
def signUp(request):

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        
        if (not(request.POST.get("TCA"))):
            context = {
            'form':signUpForm(),
            'status':'Please accept T&C'
            }
            return render(request,"signup.html",context)

        
        if User.objects.filter(email=email).exists():
            context = {
                'form': signUpForm(),
                'status': 'Email already in use'  # Displays message  
            }
            return render(request, "signup.html", context)  #Redirects   
        # create a form instance and populate it with data from the request:
        form = signUpForm(request.POST)
        # check whether it's valid:
        if (not(password == password2)): #password checker (to make sure they match.)
            context = {
            'form':form,
            'status':'Passwords do not match'  # Displays message  
            }
            return render(request,"signup.html",context)

        if form.is_valid():
            try: 
                user = User.objects.create(username = username, email = email, first_name = fname, last_name = lname) # creates account with datails inputed
                user.set_password(password) # Saves password
                user.save() # Saves account details
            except:
                context = {     #Unsuccessful singup (username is already taken)   
                'form':form,
                'status':'Username already exists'  # Displays message  
                }
                return render(request,"signup.html", context)
            
            if user is not None:  #Successful singup 
                login(request,user)
                context = {
                'form':form,
                'user':user,
                'status':'Sign Up Successful'   # Displays message  
                }
                # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {            #successful singup (for other reason)
                'form':form,
                'status':'Signup Failed'   # Displays message  
                }
                return render(request,"signup.html", context)
        else:
            form = signUpForm()        #UnSuccessful singup (inormation for signup is invalied)
            context = {
            'form':form,
            'status':'Invalid Username or Details',  # displays message  
            } 
            return render(request,"signup.html",context) 
    # if a GET (or any other method) we'll create a blank form
    return render(request,"signup.html")

        #Matthew/John 
def loginPage(request):
    # if this is a POST request we need to process the form data. Matthew 
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # create a form instance and populate it with data from the request:
        form = loginForm(request.POST)
        # check whether it's valid:
        if request.user.is_authenticated: #already login
            context = {
            'form':form,
            'status':'Already Logged In',  # displays message  
            'user': request.user,
            }
            return render(request,"home.html",context)

        if form.is_valid():
            user = authenticate(request, username=username, password=password) #login
            if user is not None:
                login(request,user)
                context = {
                'form':form,
                'user':user,
                'status':'Login Successful',  # displays message  
                }
        # Redirect to a success page.
                return render(request,"home.html",context)
            else:              #unsuccessful at login
                context = {
                'form':form,
                'status':'Invalid Username or Password' # displays message 
                }
                return render(request,"login.html", context)
        else:          #unsuccessful at login
            context = {             
            'form':form,
            'status':'Invalid Username or Password'   # displays message  
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

     #Matthew
def changePassword(request):
 # if this is a POST request we need to process the form data   
    if UserLoggedIn:
        if request.method == "POST":
            user = request.user
            oldPassword = request.POST["currentPassword"]
            password = request.POST["password"]
            password2 = request.POST["password2"]
         # create a form instance and populate it with data from the request:
            form = changePasswordForm(request.POST)
            
            if form.is_valid():
                if not(user.check_password(oldPassword)): #checks if password entred is old password
                    context = {
                    'username':GetUserName(request),
                    'status':'Incorrect Password'       # displays message 
                    }
                    return render(request,"account.html",context)
                
                if (not(password == password2)): #password checker (to make sure they match.)
                    context = {          #UnSuccessful (password dose not match)
                    'username':GetUserName(request),
                    'status':'Passwords do not match'          # displays message 
                    }
                    return render(request,"account.html",context)
                
                user.set_password(password)#set new password
                user.save() #saves new password
                context = {
                    'username':GetUserName(request),
                    'status':'Password Changed'      # displays message 
                }
                return render(request,"account.html",context) 
            else:         #UnSuccessful
                context = {
                    'username':GetUserName(request),
                    'status':'Invalid Password'             # displays message 
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

#Toby
def cancelBooking(request):

    if UserLoggedIn(request):
        if request.method == "POST": #if post
            bookingID = request.POST["bookingID"]
            
            booking = Booking.objects.filter(bookingID = bookingID).first() #get booking
            
            if booking.account != request.user: #if the booking is not the users booking
                context = {
                    'username':GetUserName(request),
                    'email':request.user.email,
                    'first_name':request.user.first_name,
                    'last_name':request.user.last_name,
                    'bookings':getUserBookings(request),
                    'status':'You cannot cancel this booking'
                }
                return render(request,"account.html",context) #return account page with message
            
            booking.delete() #delete booking
            context = {
                'username':GetUserName(request),
                'email':request.user.email,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'bookings':getUserBookings(request),
                'status':'Booking Cancelled' #success message
            }
            return render(request,"account.html",context) #return account page with message
        else:
            context = {
                'username':GetUserName(request),
                'email':request.user.email,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'bookings':getUserBookings(request), #get all user bookings
                'status':''
            }
            return render(request,"account.html",context) #return account page
    else:
        return loginPage(request) #if not logged in return login page

def bookingPage(request):
    equipment = Equipment.objects.all() #get all equipment
    if not UserLoggedIn(request):
        return loginPage(request)

    usersBookings = getUserBookings(request) #get all user bookings
    if request.method == "POST":
        #if the user wants to sort the equipment
        if request.POST["Sort"] == "Sort": #if the user wants to sort the equipment
            try: #try to get the dates
                startDate = request.POST["startDate"]
                endDate = request.POST["endDate"]
                startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date() #convert to date
                endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
            except: #if the dates are not valid
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
                return render(request,"booking.html",context) #return booking page with message

            equipment = getEquipmentBetweenDate(startDate, endDate) #get equipment that is available
            context = {
                'bookings':usersBookings,
                'equipment':equipment,
                'accountID':1,
                'itemID':1,
                'startDate':startDate,
                'endDate':endDate,
                'bookingStatus':False
            }
            return render(request,"booking.html",context)#return booking page with equipment that is available
        
        form = bookingForm(request.POST) #get the form
        if form.is_valid(): #if the form is valid
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
                'bookingStatus':bookingStatus,
                'status':'Booking Successful' #success message
            }
            context['bookingStatus'] = True #authBooking(context)
            if context['bookingStatus'] == True:
                user = User.objects.filter(id = user.id).first() #get user
                item = Equipment.objects.filter(equipmentID = itemID).first() #get equipment
                booking = Booking.create(startDate, endDate, "O", user,item) #create booking
                booking.save() #save booking
                return render(request,"booking.html",context)#return booking page with message
            
        else:
            context = {
                'bookings':usersBookings,
                'equipment':equipment,
                'accountID':1,
                'itemID':1,
                'startDate':1,
                'endDate':1,
                'bookingStatus':False,
                'status':'Booking Failed' #fail message
            }
            return render(request,"booking.html",context)#return booking page with message
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
    return render(request,"booking.html", context)#return booking page