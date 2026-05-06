from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mac_address', 'device_type', 'user', 'is_online', 'registered_at')
    search_fields = ('name', 'mac_address')
    list_filter = ('device_type', 'is_online')
