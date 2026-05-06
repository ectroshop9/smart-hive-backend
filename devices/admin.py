from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mac_address', 'device_type', 'user', 'is_online', 'registered_at')
    search_fields = ('name', 'mac_address')
    list_filter = ('device_type', 'is_online')
from .models import AuthorizedMAC

@admin.register(AuthorizedMAC)
class AuthorizedMACAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'is_registered', 'created_at')
    search_fields = ('mac_address',)
    list_filter = ('is_registered',)