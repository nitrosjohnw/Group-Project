from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Equipment(models.Model):
    # Choices for equipment locations
    LOCATIONS = [
        ("XRLBC", "XRL Lab Blue Cabinet"),
        ("XRLBCL", "XRL Lab Blue Cabinet Large"),
        ("XRL", "XRL Lab"),
        ("OTHER", "Other"),
        ('XRLMWC', "XRLab Medium Wooden Cabinet")
    ]
    
    # Choices for equipment status
    STATUS = [
        ("A", "Available"),
        ("ON", "On Loan"),
        ("D", "Decommissioned"),
        ("R", "Repairing"),
    ]

    # Equipment Details
    equipmentName = models.CharField(max_length=30, verbose_name='Name')
    equipmentType = models.CharField(max_length=30, verbose_name='Type')
    equipmentQuantity = models.IntegerField(default=1, verbose_name='Quantity')
    equipmentLocation = models.CharField(max_length=30, choices=LOCATIONS, default="OTHER", verbose_name='Location')
    equipmentAudit = models.DateField()
    equipmentStatus = models.CharField(max_length=20, choices=STATUS, default="A", verbose_name='Status')
    equipmentComment = models.CharField(max_length=200, default="")
    equipmentID = models.CharField(max_length=30, primary_key=True, verbose_name='Equip_ID')

    def __str__(self):
        return self.equipmentName + " " + self.equipmentID

    @classmethod
    def create(cls, equipmentName, equipmentType, equipmentQuantity, equipmentLocation, equipmentAudit, equipmentStatus, equipmentID):
        equipment = cls(equipmentName=equipmentName, equipmentType=equipmentType, equipmentQuantity=equipmentQuantity, equipmentLocation=equipmentLocation, equipmentAudit=equipmentAudit, equipmentStatus=equipmentStatus, equipmentID=equipmentID)
        return equipment


class Booking(models.Model):
    # Choices for booking status
    STATUS = [
        ("O", "Open"),
        ("C", "Closed"),
        ("L", "Late"),
    ]

    # Booking Details
    startDate = models.DateField()
    endDate = models.DateField()
    bookingStatus = models.CharField(max_length=10, choices=STATUS)

    # Booking Keys
    bookingID = models.AutoField(primary_key=True, null=False)
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.bookingID) + " " + self.account.username + " " + self.equipment.equipmentName

    @classmethod
    def create(cls, startDate, endDate, bookingStatus, account, equipment):
        booking = cls(startDate=startDate, endDate=endDate, bookingStatus=bookingStatus, account=account, equipment=equipment)
        return booking