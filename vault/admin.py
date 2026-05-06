from django.contrib import admin
from .models import Block

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'mac', 'block_hash_short', 'nonce', 'timestamp')
    search_fields = ('mac', 'block_hash')
    
    def block_hash_short(self, obj):
        return obj.block_hash[:16] + '...'
    block_hash_short.short_description = 'Block Hash'
