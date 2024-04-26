from django.db import models

# Create your models here.

class User_Account(models.Model):
    
    # User Account Details
    userName = models.CharField(max_length = 30)
    userPassword = models.CharField(max_length = 30)
    userEmail = models.CharField(max_length = 50)
    
    # User Account Keys
    accountID = models.CharField(max_length = 30, primary_key = True)
    userFK = models.ForeignKey('Admin_Account', on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.accountID

class Admin_Account(models.Model):
    
    # Admin Account Details
    adminName = models.CharField(max_length = 30)
    adminPassword = models.CharField(max_length = 30)
    adminEmail = models.CharField(max_length = 50)
    
    # Admin Account Keys
    accountID = models.CharField(max_length = 30, primary_key = True)
    #adminID = models.CharField(max_length = 30, alternate_key = True )
    
    def __str__(self):
        return self.accountID
    
class Booking(models.Model):
    
    STATUS = [
        ("O", "Open"),
        ("C", "Closed"),
        ("L", "Late"),
    ]

    # Booking Details
    startDate = models.CharField(max_length = 10)
    endDate = models.CharField(max_length = 10)
    bookingStatus = models.CharField(max_length = 10, choices = STATUS)
    
    # Booking Keys
    bookingID = models.CharField(max_length = 30, primary_key = True)
    accountID = models.ForeignKey('User_Account', on_delete = models.SET_NULL, null = True)
    equipmentID = models.ForeignKey('Equipment', on_delete = models.SET_NULL, null = True)
    #adminID = models.ForeignKey('Admin_Account', on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.bookingID  
        
    @classmethod
    def create(cls, startDate, endDate, bookingStatus, bookingID, accountID):
        booking = cls(startDate=startDate, endDate=endDate, bookingStatus = bookingStatus, bookingID =bookingID, accountID = accountID)
        return booking
    
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