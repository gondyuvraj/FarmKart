from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hindi_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, default='🌱')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.hindi_name})" if self.hindi_name else self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    hindi_name = models.CharField(max_length=200, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50, blank=True, default='1 Unit')
    crop_type = models.CharField(max_length=250, blank=True)
    dosage = models.CharField(max_length=250, blank=True)
    application_method = models.CharField(max_length=100, blank=True, default='Foliar Spray')
    is_organic = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def sale_price(self):
        discount_factor = Decimal(str(self.discount)) / Decimal('100')
        return round(self.price - (self.price * discount_factor), 2)

    @property
    def save_amount(self):
        return round(self.price - self.sale_price, 2)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wished_by')
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
