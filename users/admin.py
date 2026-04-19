from django.contrib import admin
from .models import Beekeeper

@admin.register(Beekeeper)
class BeekeeperAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'phone', 'is_active', 'registered_at']
    list_filter = ['is_active']
    search_fields = ['user_id', 'name', 'phone']
