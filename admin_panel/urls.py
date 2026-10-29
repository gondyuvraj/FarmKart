from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.admin_products_list, name='admin_products_list'),
    path('products/add/', views.admin_product_add, name='admin_product_add'),
    path('products/<str:pk>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('products/<str:pk>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('products/<str:pk>/quick-stock/', views.admin_product_quick_stock, name='admin_product_quick_stock'),
    path('orders/', views.admin_orders_list, name='admin_orders_list'),
    path('orders/<str:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('categories/', views.admin_categories_list, name='admin_categories_list'),
    path('customers/', views.admin_customers_list, name='admin_customers_list'),
    path('reviews/', views.admin_reviews_list, name='admin_reviews_list'),
    path('announcements/', views.admin_announcements, name='admin_announcements'),
]
