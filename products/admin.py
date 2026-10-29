from django.contrib import admin
from .models import Category, Product, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'hindi_name', 'icon')
    search_fields = ('name', 'hindi_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'discount', 'sale_price', 'stock', 'unit', 'is_organic', 'is_featured', 'is_best_seller', 'rating')
    search_fields = ('name', 'hindi_name', 'brand', 'crop_type')
    list_filter = ('category', 'is_organic', 'is_featured', 'is_best_seller')
    list_editable = ('price', 'discount', 'stock', 'is_featured', 'is_best_seller')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
