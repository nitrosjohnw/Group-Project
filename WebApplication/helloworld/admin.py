from django.contrib import admin
from helloworld.models import Equipment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import  colors

#reports method
def download_pdf(self,request, queryset):
    model_name = self.model.__name__
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'attachment; filename = {model_name}.pdf'

    pdf = canvas.Canvas(response,pagesize = letter)
    pdf.setTitle('PDF Report')
    
    #creating table
    headers = [field.verbose_name for field in self.model._meta.fields]
    data = [headers]

    for obj in queryset:
        data_row = [str (getattr(obj,field.name)) for field in self.model._meta.fields]
        data.append(data_row)

    table = Table(data)
    table.setStyle(TableStyle(
        [
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]
    ))

    canvas_width = 600
    canvas_height = 600

    table.wrapOn(pdf,canvas_width,canvas_height)
    table.drawOn(pdf,10,canvas_height - len(data))
    
    pdf.save()
    return response
download_pdf.short_description = "Download selected items as PDF"
# Register your models here.
# Path: WebApplication/helloworld/admin.py

from .models import  Booking, Equipment

admin.site.register(Booking)
#admin.site.register(Equipment)
#changed to the one below for the reports functionality
@admin.register(Equipment)
class Equipmentadmin(admin.ModelAdmin):
    actions = [download_pdf]