from django.contrib import admin
from .models import SensorReading

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'device', 'timestamp', 'temperature_1', 'weight', 'battery_level', 'state']
    list_filter = ['state', 'device__device_type']
    search_fields = ['device__device_id']
    date_hierarchy = 'timestamp'
