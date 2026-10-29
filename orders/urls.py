from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/<str:pk>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<str:pk>/', views.order_detail, name='order_detail'),
    path('order/<str:pk>/invoice/', views.order_invoice, name='order_invoice'),
    path('order/<str:pk>/cancel/', views.cancel_order, name='cancel_order'),
]
