from django.contrib import admin

# Register your models here.
# Path: WebApplication/helloworld/admin.py

from .models import User_Account, Admin_Account, Booking, Equipment

admin.site.register(User_Account,Admin_Account,Booking,Equipment)
