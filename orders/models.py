from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    STATUS = [
        ('PLACED', 'Order Placed (ऑर्डर दर्ज)'),
        ('CONFIRMED', 'Order Confirmed (पुष्टि की गई)'),
        ('SHIPPED', 'Dispatched / In Transit (मार्ग में)'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery (डिलीवरी के लिए निकला)'),
        ('DELIVERED', 'Delivered (सफलतापूर्वक वितरित)'),
        ('CANCELLED', 'Cancelled (रद्द)'),
    ]

    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery (पे ऑन डिलीवरी)'),
        ('UPI', 'UPI / QR Scan (PhonePe, GPay, Paytm)'),
        ('NETBANKING', 'Kisan Credit Card (KCC) / NetBanking'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=150, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS, default='PLACED')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='COD')
    payment_status = models.CharField(max_length=20, default='PENDING', choices=[('PENDING', 'Pending'), ('PAID', 'Paid')])
    expected_delivery = models.CharField(max_length=50, blank=True, default='2 - 4 Business Days')
    tracking_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def order_number(self):
        return f"FK-{str(self.id)[-6:].upper()}"

    def __str__(self):
        return f"{self.order_number} ({self.name})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        prod_name = self.product.name if self.product else "Discontinued Item"
        return f"{prod_name} × {self.quantity}"
