# store/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage, SavedItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Show 3 empty forms for adding images

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'created', 'updated')
    list_filter = ('category', 'created')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(SavedItem)

# cart/admin.py

from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_price')
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)

# users/admin.py

from django.contrib import admin
from .models import Profile

admin.site.register(Profile)