from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.api import product_api

urlpatterns=[
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('payments/', include('payments.urls')),
    path('api/products/', product_api),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
