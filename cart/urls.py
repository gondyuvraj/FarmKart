from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<str:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update/<str:pk>/', views.update_cart, name='update_cart'),
    path('remove/<str:pk>/', views.remove_from_cart, name='remove_from_cart'),
]
