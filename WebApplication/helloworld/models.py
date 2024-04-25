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
    # Equipment Details
    equipmentName = models.CharField(max_length = 30)
    equipmentType = models.CharField(max_length = 30)
    equipmentAssests = models.CharField(max_length = 30)
    equipmentStatus = models.CharField(max_length = 30)
    equipmentWarranty = models.CharField(max_length = 30)
    equipmentOnSite = models.BooleanField()
    equipmentAudit =  models.CharField(max_length = 30)
    
    equipmentID = models.CharField(max_length = 30, primary_key = True)
    
    def __str__(self):
        return self.equipmentID  
    
    @classmethod
    def create(cls, equipmentName, equipmentType, equipmentAssests, equipmentStatus, equipmentWarranty, equipmentOnSite, equipmentAudit, equipmentID):
        equipment = cls(equipmentName=equipmentName, equipmentType=equipmentType, equipmentAssests = equipmentAssests, equipmentStatus = equipmentStatus, equipmentWarranty = equipmentWarranty, equipmentOnSite = equipmentOnSite, equipmentAudit = equipmentAudit, equipmentID = equipmentID)
        return equipment
    