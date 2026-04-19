from django.contrib import admin
from .models import SerialKey

@admin.register(SerialKey)
class SerialKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'is_used', 'used_by', 'used_at', 'created_at']
    list_filter = ['is_used']
    search_fields = ['key', 'used_by__email']
    readonly_fields = ['key', 'created_at']
    actions = ['generate_new_keys']
    
    def generate_new_keys(self, request, queryset):
        from .models import generate_serial_key
        key = SerialKey.objects.create()
        self.message_user(request, f'✅ تم إنشاء مفتاح جديد: {key.key}')
    generate_new_keys.short_description = "توليد مفتاح جديد"
