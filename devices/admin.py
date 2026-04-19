from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'device_type', 'user', 'firmware_version', 'is_online', 'last_seen']
    list_filter = ['device_type', 'is_online']
    search_fields = ['device_id', 'name', 'user__name']
