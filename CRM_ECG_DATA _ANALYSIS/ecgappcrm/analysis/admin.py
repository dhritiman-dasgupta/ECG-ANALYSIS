# healthapp/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Patient, ecgdata, Device

class EcgDataInline(admin.TabularInline):
    model = ecgdata
    extra = 0
    readonly_fields = ('scan_data', 'EventProcessedUtcTime')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'last_name', 'contact_number', 'device_id', 'age', 'view_scan_data')
    inlines = [EcgDataInline]

    def view_scan_data(self, obj):
        # Create a link to view the scan data
        url = reverse('admin:healthapp_ecgdata_changelist') + f'?device_id={obj.device_id}'
        return format_html('<a href="{}">View Scan Data</a>', url)

    view_scan_data.short_description = 'Scan Data'

admin.site.register(Patient, PatientAdmin)
admin.site.register(ecgdata)
admin.site.register(Device)
