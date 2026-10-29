from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100, blank=True, default='Maharashtra')
    district = models.CharField(max_length=100, blank=True)
    primary_crop = models.CharField(max_length=100, blank=True, default='Wheat')
    land_size = models.CharField(max_length=50, blank=True, default='2 - 5 Acres')
    is_verified_farmer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.phone})"
