import json
import os
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.core.files.storage import default_storage

from products.models import Product, Category
from orders.models import Order, OrderItem
from reviews.models import Review
from .decorators import admin_required

ANNOUNCEMENT_FILE = settings.BASE_DIR / 'media' / 'store_announcement.json'

def get_announcement_data():
    """Retrieve current store announcement banner configuration."""
    default_data = {
        'headline': '🌾 Kisan Call Center: 1800-180-1551 (Toll-Free 6 AM - 10 PM) · 🚜 Free Delivery on orders over ₹999',
        'subline': '● 100% Certified Agri-Inputs · Government Subsidy Assistance Available',
        'is_active': True,
        'alert_banner': '📢 Special Seasonal Offer: Flat 20% discount on Hybrid Certified Seeds & Bio-Pesticides!'
    }
    if os.path.exists(ANNOUNCEMENT_FILE):
        try:
            with open(ANNOUNCEMENT_FILE, 'r', encoding='utf-8') as f:
                return {**default_data, **json.load(f)}
        except Exception:
            return default_data
    return default_data

def save_announcement_data(data):
    """Save store announcement banner configuration."""
    os.makedirs(os.path.dirname(ANNOUNCEMENT_FILE), exist_ok=True)
    with open(ANNOUNCEMENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@admin_required
def admin_dashboard(request):
    """Admin Control Center Overview & Business Metrics."""
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()

    # Calculate Total Revenue (excluding cancelled orders)
    active_orders = Order.objects.exclude(status='CANCELLED')
    total_revenue = sum(o.total for o in active_orders)

    # Order status counts
    placed_count = Order.objects.filter(status='PLACED').count()
    confirmed_count = Order.objects.filter(status='CONFIRMED').count()
    shipped_count = Order.objects.filter(status='SHIPPED').count()
    delivered_count = Order.objects.filter(status='DELIVERED').count()
    cancelled_count = Order.objects.filter(status='CANCELLED').count()

    # Low stock alerts (< 10 units)
    low_stock_products = Product.objects.filter(stock__lte=10).order_by('stock')[:8]
    out_of_stock_count = Product.objects.filter(stock=0).count()

    # Recent Orders
    recent_orders = Order.objects.order_by('-created_at')[:8]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'placed_count': placed_count,
        'confirmed_count': confirmed_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'cancelled_count': cancelled_count,
        'low_stock_products': low_stock_products,
        'out_of_stock_count': out_of_stock_count,
        'recent_orders': recent_orders,
        'announcement': get_announcement_data(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def admin_products_list(request):
    """Admin Product Inventory Management with search, filter, and quick stock edit."""
    q = request.GET.get('q', '').strip()
    cat_id = request.GET.get('category', '').strip()
    stock_status = request.GET.get('stock', '').strip()

    products = Product.objects.all().order_by('-created_at')

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(brand__icontains=q) |
            Q(hindi_name__icontains=q) |
            Q(crop_type__icontains=q)
        )

    if cat_id:
        products = products.filter(category_id=cat_id)

    if stock_status == 'low':
        products = products.filter(stock__gt=0, stock__lte=10)
    elif stock_status == 'out':
        products = products.filter(stock=0)
    elif stock_status == 'in':
        products = products.filter(stock__gt=10)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'q': q,
        'cat_id': cat_id,
        'stock_status': stock_status,
        'total_count': products.count(),
    }
    return render(request, 'admin_panel/products_list.html', context)


@admin_required
def admin_product_add(request):
    """Admin: Add New Agricultural Product."""
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        hindi_name = request.POST.get('hindi_name', '').strip()
        brand = request.POST.get('brand', '').strip()
        category_id = request.POST.get('category', '').strip()
        price = request.POST.get('price', '0').strip()
        discount = request.POST.get('discount', '0').strip()
        stock = request.POST.get('stock', '0').strip()
        unit = request.POST.get('unit', '1 Unit').strip()
        crop_type = request.POST.get('crop_type', '').strip()
        dosage = request.POST.get('dosage', '').strip()
        application_method = request.POST.get('application_method', 'Foliar Spray').strip()
        description = request.POST.get('description', '').strip()
        is_organic = request.POST.get('is_organic') == '1'
        is_featured = request.POST.get('is_featured') == '1'
        is_best_seller = request.POST.get('is_best_seller') == '1'
        image = request.FILES.get('image')

        if not name or not price or not category_id:
            messages.error(request, 'Product Name, Price, and Category are mandatory.')
            return render(request, 'admin_panel/product_form.html', {'categories': categories, 'is_edit': False})

        category = get_object_or_404(Category, pk=category_id)

        try:
            product = Product.objects.create(
                category=category,
                name=name,
                hindi_name=hindi_name,
                brand=brand,
                price=Decimal(price),
                discount=Decimal(discount or '0'),
                stock=int(stock or 0),
                unit=unit,
                crop_type=crop_type,
                dosage=dosage,
                application_method=application_method,
                description=description,
                is_organic=is_organic,
                is_featured=is_featured,
                is_best_seller=is_best_seller,
                image=image
            )
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('admin_products_list')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')

    return render(request, 'admin_panel/product_form.html', {'categories': categories, 'is_edit': False})


@admin_required
def admin_product_edit(request, pk):
    """Admin: Edit Existing Agricultural Product."""
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        hindi_name = request.POST.get('hindi_name', '').strip()
        brand = request.POST.get('brand', '').strip()
        category_id = request.POST.get('category', '').strip()
        price = request.POST.get('price', '0').strip()
        discount = request.POST.get('discount', '0').strip()
        stock = request.POST.get('stock', '0').strip()
        unit = request.POST.get('unit', '1 Unit').strip()
        crop_type = request.POST.get('crop_type', '').strip()
        dosage = request.POST.get('dosage', '').strip()
        application_method = request.POST.get('application_method', 'Foliar Spray').strip()
        description = request.POST.get('description', '').strip()
        is_organic = request.POST.get('is_organic') == '1'
        is_featured = request.POST.get('is_featured') == '1'
        is_best_seller = request.POST.get('is_best_seller') == '1'
        image = request.FILES.get('image')

        if not name or not price or not category_id:
            messages.error(request, 'Product Name, Price, and Category are mandatory.')
            return render(request, 'admin_panel/product_form.html', {'product': product, 'categories': categories, 'is_edit': True})

        try:
            product.category = get_object_or_404(Category, pk=category_id)
            product.name = name
            product.hindi_name = hindi_name
            product.brand = brand
            product.price = Decimal(price)
            product.discount = Decimal(discount or '0')
            product.stock = int(stock or 0)
            product.unit = unit
            product.crop_type = crop_type
            product.dosage = dosage
            product.application_method = application_method
            product.description = description
            product.is_organic = is_organic
            product.is_featured = is_featured
            product.is_best_seller = is_best_seller
            if image:
                product.image = image
            product.save()

            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('admin_products_list')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    return render(request, 'admin_panel/product_form.html', {'product': product, 'categories': categories, 'is_edit': True})


@admin_required
def admin_product_quick_stock(request, pk):
    """Admin: Quick inline stock and price update without full edit page."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        try:
            stock = int(request.POST.get('stock', product.stock))
            price = Decimal(request.POST.get('price', str(product.price)))
            discount = Decimal(request.POST.get('discount', str(product.discount)))
            product.stock = max(0, stock)
            product.price = price
            product.discount = discount
            product.save(update_fields=['stock', 'price', 'discount'])
            messages.success(request, f'Updated {product.name} stock to {stock} & price to ₹{price}.')
        except Exception as e:
            messages.error(request, f'Update failed: {str(e)}')
    return redirect(request.META.get('HTTP_REFERER', 'admin_products_list'))


@admin_required
def admin_product_delete(request, pk):
    """Admin: Delete Product."""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" was deleted successfully.')
    return redirect('admin_products_list')


@admin_required
def admin_orders_list(request):
    """Admin: Order Management with status filters and customer search."""
    status_filter = request.GET.get('status', '').strip()
    payment_filter = request.GET.get('payment', '').strip()
    q = request.GET.get('q', '').strip()

    orders = Order.objects.all().order_by('-created_at')

    if status_filter:
        orders = orders.filter(status=status_filter)

    if payment_filter:
        orders = orders.filter(payment_method=payment_filter)

    if q:
        orders = orders.filter(
            Q(name__icontains=q) |
            Q(phone__icontains=q) |
            Q(city__icontains=q) |
            Q(pincode__icontains=q)
        )

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'payment_filter': payment_filter,
        'q': q,
        'total_count': orders.count(),
        'status_choices': Order.STATUS,
    }
    return render(request, 'admin_panel/orders_list.html', context)


@admin_required
def admin_order_detail(request, pk):
    """Admin: Order fulfillment, tracking update, and status change."""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()
        tracking_number = request.POST.get('tracking_number', '').strip()
        expected_delivery = request.POST.get('expected_delivery', '').strip()
        payment_status = request.POST.get('payment_status', '').strip()
        notes = request.POST.get('notes', '').strip()

        if new_status:
            order.status = new_status
        if tracking_number:
            order.tracking_number = tracking_number
        if expected_delivery:
            order.expected_delivery = expected_delivery
        if payment_status:
            order.payment_status = payment_status
        order.notes = notes
        order.save()

        messages.success(request, f'Order #{order.order_number} details updated successfully!')
        return redirect('admin_order_detail', pk=pk)

    context = {
        'order': order,
        'status_choices': Order.STATUS,
        'payment_status_choices': [('PENDING', 'Pending'), ('PAID', 'Paid')],
    }
    return render(request, 'admin_panel/order_detail.html', context)


@admin_required
def admin_categories_list(request):
    """Admin: Category Management (Add, Edit, View counts)."""
    categories = Category.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name', '').strip()
            hindi_name = request.POST.get('hindi_name', '').strip()
            icon = request.POST.get('icon', '🌱').strip()
            desc = request.POST.get('description', '').strip()
            if name:
                Category.objects.create(name=name, hindi_name=hindi_name, icon=icon, description=desc)
                messages.success(request, f'Category "{name}" added successfully.')
            else:
                messages.error(request, 'Category name is required.')
        elif action == 'edit':
            cat_id = request.POST.get('category_id')
            cat = get_object_or_404(Category, pk=cat_id)
            cat.name = request.POST.get('name', cat.name).strip()
            cat.hindi_name = request.POST.get('hindi_name', cat.hindi_name).strip()
            cat.icon = request.POST.get('icon', cat.icon).strip()
            cat.description = request.POST.get('description', cat.description).strip()
            cat.save()
            messages.success(request, f'Category "{cat.name}" updated.')
        elif action == 'delete':
            cat_id = request.POST.get('category_id')
            cat = get_object_or_404(Category, pk=cat_id)
            name = cat.name
            cat.delete()
            messages.success(request, f'Category "{name}" deleted.')
        return redirect('admin_categories_list')

    # Attach product counts to each category
    cat_data = []
    for c in categories:
        count = Product.objects.filter(category=c).count()
        cat_data.append({'cat': c, 'product_count': count})

    return render(request, 'admin_panel/categories_list.html', {'categories': cat_data})


@admin_required
def admin_customers_list(request):
    """Admin: Registered Farmers & Customers Directory with order stats."""
    q = request.GET.get('q', '').strip()
    users = User.objects.all().order_by('-date_joined')

    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(email__icontains=q)
        )

    customer_data = []
    for u in users:
        orders = Order.objects.filter(user=u)
        orders_count = orders.count()
        total_spend = sum(o.total for o in orders.exclude(status='CANCELLED'))
        customer_data.append({
            'user': u,
            'orders_count': orders_count,
            'total_spend': total_spend,
            'latest_order': orders.order_by('-created_at').first(),
        })

    context = {
        'customers': customer_data,
        'q': q,
        'total_count': users.count(),
    }
    return render(request, 'admin_panel/customers_list.html', context)


@admin_required
def admin_reviews_list(request):
    """Admin: Customer Reviews Moderation."""
    reviews = Review.objects.all().order_by('-created_at')

    if request.method == 'POST':
        action = request.POST.get('action')
        review_id = request.POST.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        if action == 'delete':
            prod = review.product
            review.delete()
            # Recalculate rating
            rem_reviews = prod.reviews.all()
            if rem_reviews.exists():
                prod.rating = round(sum(r.rating for r in rem_reviews) / rem_reviews.count(), 1)
                prod.review_count = rem_reviews.count()
            else:
                prod.rating = Decimal('0')
                prod.review_count = 0
            prod.save()
            messages.success(request, 'Customer review removed.')
        return redirect('admin_reviews_list')

    return render(request, 'admin_panel/reviews_list.html', {'reviews': reviews})


@admin_required
def admin_announcements(request):
    """Admin: Store Announcements & Kisan Information Control."""
    current_data = get_announcement_data()

    if request.method == 'POST':
        headline = request.POST.get('headline', '').strip()
        subline = request.POST.get('subline', '').strip()
        alert_banner = request.POST.get('alert_banner', '').strip()
        is_active = request.POST.get('is_active') == '1'

        new_data = {
            'headline': headline or current_data['headline'],
            'subline': subline or current_data['subline'],
            'alert_banner': alert_banner,
            'is_active': is_active
        }
        save_announcement_data(new_data)
        messages.success(request, 'Store information announcements updated and broadcasted across website!')
        return redirect('admin_announcements')

    return render(request, 'admin_panel/announcements.html', {'announcement': current_data})
