# cart/admin.py (updated to include orders)

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_price')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'total_price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'status', 'payment_method', 'total_price', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Order Details', {
            'fields': ('address', 'payment_method', 'status', 'created_at', 'updated_at', 'total_price')
        }),
    )

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)