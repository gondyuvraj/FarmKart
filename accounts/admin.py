from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'state', 'primary_crop', 'land_size', 'is_verified_farmer', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'phone', 'state', 'primary_crop')
    list_filter = ('state', 'primary_crop', 'is_verified_farmer')
