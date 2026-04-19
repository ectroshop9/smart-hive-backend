from django.contrib import admin
from .models import Firmware

@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ['firmware_id', 'version', 'device_type', 'is_stable', 'uploaded_at']
    list_filter = ['device_type', 'is_stable']
    search_fields = ['version']
from .models import OTASession

@admin.register(OTASession)
class OTASessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'device', 'firmware', 'status', 'progress', 'started_at', 'completed_at']
    list_filter = ['status']
    search_fields = ['device__device_id']
    readonly_fields = ['started_at']
