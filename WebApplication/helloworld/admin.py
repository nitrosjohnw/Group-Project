from django.contrib import admin

# Register your models here.
# Path: WebApplication/helloworld/admin.py

from .models import  Booking, Equipment

admin.site.register(Booking)
admin.site.register(Equipment)
