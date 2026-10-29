from django.contrib import admin
from .models import Order, OrderItem

class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'name', 'phone', 'city', 'state', 'total', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('name', 'phone', 'city', 'pincode', 'id')
    list_editable = ('status',)
    inlines = [ItemInline]
