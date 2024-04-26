from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Equipment(models.Model):
    LOCATIONS = [
        ("XRLBC", "XRL Lab Blue Cabinet"),
        ("XRLBCL", "XRL Lab Blue Cabinet Large"),
        ("XRL", "XRL Lab"),
        ("OTHER", "Other"),
        ('XRLMWC', "XRLab Medium Wooden Cabinet")
    ]
    STATUS = [
        ("A", "Available"),
        ("ON", "On Loan"),
        ("D", "Decommissioned"),
        ("R", "Repairing"),
    ]

    # Equipment Details
    equipmentName = models.CharField(max_length = 30)
    equipmentType = models.CharField(max_length = 30)
    equipmentQuantity = models.IntegerField( default= 1)
    equipmentLocation = models.CharField(max_length = 30, choices = LOCATIONS , default = "OTHER")
    equipmentAudit =  models.DateField()
    equipmentStatus = models.CharField(max_length = 20, choices = STATUS, default = "A")

    equipmentID = models.CharField(max_length = 30, primary_key = True)
    
    def __str__(self):
        return self.equipmentID  
    
    @classmethod
    def create(cls, equipmentName, equipmentType, equipmentQuantity, equipmentLocation, equipmentAudit, equipmentStatus, equipmentID):
        equipment = cls(equipmentName=equipmentName, equipmentType=equipmentType, equipmentQuantity = equipmentQuantity, equipmentLocation = equipmentLocation, equipmentAudit = equipmentAudit, equipmentStatus = equipmentStatus, equipmentID = equipmentID)
        return equipment

class Booking(models.Model):
    
    STATUS = [
        ("O", "Open"),
        ("C", "Closed"),
        ("L", "Late"),
    ]

    # Booking Details
    startDate = models.DateField()
    endDate = models.DateField()
    bookingStatus = models.CharField(max_length = 10, choices = STATUS)
    
    # Booking Keys
    bookingID = models.AutoField(primary_key = True, null = False)
    account = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    equipment = models.ForeignKey(Equipment, on_delete = models.SET_NULL, null = True)
    #adminID = models.ForeignKey('Admin_Account', on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.bookingStatus  
        
    @classmethod
    def create(cls, startDate, endDate, bookingStatus, account, equipment):
        print("Creating Booking")
        print(startDate)
        print(endDate)
        print(bookingStatus)
        print(account)
        print(equipment)
        booking = cls(startDate=startDate, endDate=endDate, bookingStatus = bookingStatus, account = account, equipment = equipment)
        return booking
