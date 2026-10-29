from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    crop_used_on = models.CharField(max_length=150, blank=True)
    is_verified_farmer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate average rating for product
        reviews = self.product.reviews.all()
        count = reviews.count()
        if count > 0:
            total_stars = sum(r.rating for r in reviews)
            self.product.rating = round(total_stars / count, 1)
            self.product.review_count = count
            self.product.save(update_fields=['rating', 'review_count'])

    def __str__(self):
        return f"{self.user.username} ({self.rating}★) on {self.product.name}"
