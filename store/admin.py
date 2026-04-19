from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'category', 'price', 'stock_quantity', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['product_id', 'name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'total_amount', 'status', 'order_date']
    list_filter = ['status']
    search_fields = ['order_id', 'user__name']
    inlines = [OrderItemInline]
