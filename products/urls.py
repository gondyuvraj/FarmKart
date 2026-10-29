from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<str:pk>/', views.product_detail, name='product_detail'),
    path('wishlist/<str:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('my-wishlist/', views.my_wishlist, name='my_wishlist'),
    path('calculator/', views.agri_calculator, name='agri_calculator'),
]
