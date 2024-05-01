from django.contrib import admin
from helloworld.models import Equipment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate ,Table, TableStyle, PageBreak
from reportlab.lib import  colors
from reportlab.lib.styles import  getSampleStyleSheet

#reports method
def download_pdf(self, request, queryset):
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Get the sample style sheet for setting table styles
    styles = getSampleStyleSheet()

    # Create table header
    headers = [field.verbose_name for field in self.model._meta.fields]
    data = [headers]

    # Add data rows
    for obj in queryset:
        data_row = [str(getattr(obj, field.name)) for field in self.model._meta.fields]
        data.append(data_row)

    # Calculate how many rows can fit on a single page
    rows_per_page = 50  # Adjust this value based on your content and page size

    # Split data into chunks for multiple pages
    for i in range(0, len(data), rows_per_page):
        chunk = data[i:i + rows_per_page]

        # Create table for each chunk
        table = Table(chunk)
        table.setStyle(TableStyle([
            ('BACKGROUND', (1, 1), (1, -1), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(PageBreak())

    pdf.build(elements)
    return response
download_pdf.short_description = "Download selected items as PDF"
# Register your models here.
# Path: WebApplication/helloworld/admin.py

# Booking.objects.filter(ITEM HERE)

from .models import  Booking, Equipment

admin.site.register(Booking)
#admin.site.register(Equipment)
#changed to the one below for the reports functionality
@admin.register(Equipment)
class Equipmentadmin(admin.ModelAdmin):
    actions = [download_pdf]