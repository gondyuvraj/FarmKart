from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'crop_used_on', 'is_verified_farmer', 'created_at')
    list_filter = ('rating', 'is_verified_farmer', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment', 'crop_used_on')
