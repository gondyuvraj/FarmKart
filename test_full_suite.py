import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmkart.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from django.template.loader import get_template
from django.contrib.auth.models import User
from products.models import Product, Category, Wishlist
from orders.models import Order, OrderItem
from reviews.models import Review
from accounts.models import UserProfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def log(msg, success=True):
    symbol = "[PASS]" if success else "[FAIL]"
    print(f"{symbol} {msg}")

def test_template_compilation():
    print("\n--- 1. Testing Template Compilation ---")
    templates = [
        'base.html',
        'accounts/login.html',
        'accounts/profile.html',
        'accounts/register.html',
        'admin_panel/announcements.html',
        'admin_panel/base_admin.html',
        'admin_panel/categories_list.html',
        'admin_panel/customers_list.html',
        'admin_panel/dashboard.html',
        'admin_panel/orders_list.html',
        'admin_panel/order_detail.html',
        'admin_panel/products_list.html',
        'admin_panel/product_form.html',
        'admin_panel/reviews_list.html',
        'cart/cart.html',
        'orders/checkout.html',
        'orders/my_orders.html',
        'orders/order_detail.html',
        'orders/order_invoice.html',
        'orders/order_success.html',
        'products/calculator.html',
        'products/home.html',
        'products/my_wishlist.html',
        'products/product_detail.html',
        'products/product_list.html',
    ]
    for t_name in templates:
        try:
            t = get_template(t_name)
            log(f"Template compiled cleanly: {t_name}")
        except Exception as e:
            log(f"Template compilation failed for {t_name}: {e}", success=False)
            return False
    return True

def test_public_pages_and_api(client):
    print("\n--- 2. Testing Public URLs & REST API ---")
    first_product = Product.objects.first()
    first_product_id = str(first_product.id) if first_product else None

    urls = [
        ('/', 200, "Home page"),
        ('/products/', 200, "Product list"),
        ('/calculator/', 200, "Agri Calculator"),
        ('/calculator/?crop=wheat&acres=3', 200, "Agri Calculator with wheat 3 acres"),
        ('/cart/', 200, "Shopping cart page"),
        ('/accounts/login/', 200, "Login page"),
        ('/accounts/register/', 200, "Register page"),
        ('/api/products/', 200, "REST API endpoint"),
    ]
    if first_product_id:
        urls.append((f'/products/{first_product_id}/', 200, f"Product detail ({first_product.name})"))

    all_passed = True
    for url, expected_status, desc in urls:
        resp = client.get(url)
        if resp.status_code == expected_status:
            log(f"GET {url} [{desc}] -> HTTP {resp.status_code}")
        else:
            log(f"GET {url} [{desc}] -> Expected {expected_status}, got {resp.status_code}", success=False)
            all_passed = False
    return all_passed

def test_crud_operations(client):
    print("\n--- 3. Testing Full CRUD Operations & Business Logic ---")
    # Clean up any leftover test data
    User.objects.filter(username__startswith='test_').delete()
    Category.objects.filter(name='Test Category QA').delete()
    Product.objects.filter(name='Test Agri Product QA').delete()

    # A. User Registration & Profile CRUD
    print("-> A. Testing User Account CRUD")
    user = User.objects.create_user(
        username='test_farmer_qa',
        email='test_farmer@example.com',
        password='TestPassword123!',
        first_name='Ramesh'
    )
    profile = UserProfile.objects.create(
        user=user,
        phone='9876543210',
        state='Punjab',
        district='Ludhiana',
        primary_crop='Wheat',
        land_size='10 Acres',
        is_verified_farmer=True
    )
    log(f"Created User: {user.username} & UserProfile: {profile.phone}")

    # Read profile
    fetched_user = User.objects.get(username='test_farmer_qa')
    assert fetched_user.profile.district == 'Ludhiana'
    log(f"Read UserProfile: {fetched_user.profile.district}")

    # Update profile
    fetched_user.profile.district = 'Amritsar'
    fetched_user.profile.save()
    assert UserProfile.objects.get(user=user).district == 'Amritsar'
    log("Updated UserProfile district to Amritsar")

    # B. Category CRUD
    print("-> B. Testing Category CRUD")
    cat = Category.objects.create(
        name='Test Category QA',
        hindi_name='परीक्षण श्रेणी',
        icon='🌾',
        description='Automated test category'
    )
    log(f"Created Category: {cat.name} (id={cat.id})")

    cat.hindi_name = 'अपडेटेड श्रेणी'
    cat.save()
    assert Category.objects.get(pk=cat.pk).hindi_name == 'अपडेटेड श्रेणी'
    log("Updated Category hindi_name")

    # C. Product CRUD
    print("-> C. Testing Product CRUD")
    prod = Product.objects.create(
        category=cat,
        name='Test Agri Product QA',
        hindi_name='परीक्षण उत्पाद',
        brand='FarmKart Lab',
        price=Decimal('500.00'),
        discount=Decimal('10.00'),
        stock=50,
        unit='1 Kg Pack',
        crop_type='Wheat, Rice',
        dosage='500g per acre',
        application_method='Foliar Spray',
        description='Top grade agri test input',
        is_organic=True,
        is_featured=True
    )
    log(f"Created Product: {prod.name} (Sale price: ₹{prod.sale_price})")
    assert prod.sale_price == Decimal('450.00')

    # Update Product
    prod.stock = 45
    prod.price = Decimal('550.00')
    prod.save()
    assert Product.objects.get(pk=prod.pk).stock == 45
    log("Updated Product stock & price")

    # D. Cart CRUD (Session)
    print("-> D. Testing Shopping Cart CRUD")
    client.force_login(user)

    # Add to cart
    resp = client.post(f'/cart/add/{prod.pk}/', {'quantity': 2})
    assert resp.status_code == 302
    session = client.session
    cart = session.get('cart', {})
    assert cart.get(str(prod.pk)) == 2
    log(f"Added product to cart (qty=2)")

    # Update cart qty
    resp = client.post(f'/cart/update/{prod.pk}/', {'action': 'increase'})
    assert resp.status_code == 302
    session = client.session
    assert session['cart'].get(str(prod.pk)) == 3
    log(f"Increased cart qty to 3")

    # E. Order Placement & Stock Management
    print("-> E. Testing Order Placement, Stock Reduction & Tracking")
    initial_stock = Product.objects.get(pk=prod.pk).stock
    checkout_data = {
        'name': 'Ramesh Kumar',
        'phone': '9876543210',
        'address': 'Plot 45, Green Fields Village',
        'city': 'Ludhiana',
        'state': 'Punjab',
        'pincode': '141001',
        'landmark': 'Near Kisan Mandi',
        'payment_method': 'COD',
        'notes': 'Deliver before noon',
    }
    resp = client.post('/orders/checkout/', checkout_data)
    assert resp.status_code == 302
    log("Checkout form submitted successfully")

    # Verify order created
    order = Order.objects.filter(user=user).latest('created_at')
    assert order.name == 'Ramesh Kumar'
    assert order.status == 'CONFIRMED'
    log(f"Order created: #{order.order_number} for ₹{order.total}")

    # Verify stock reduction
    updated_prod = Product.objects.get(pk=prod.pk)
    assert updated_prod.stock == initial_stock - 3
    log(f"Stock correctly decremented from {initial_stock} to {updated_prod.stock}")

    # F. Order Cancellation & Stock Restoration
    print("-> F. Testing Order Cancellation & Stock Restoration")
    cancel_url = reverse('cancel_order', kwargs={'pk': str(order.pk)})
    resp = client.post(cancel_url)
    assert resp.status_code == 302
    order.refresh_from_db()
    assert order.status == 'CANCELLED'
    updated_prod.refresh_from_db()
    assert updated_prod.stock == initial_stock
    log(f"Order #{order.order_number} cancelled, stock restored to {updated_prod.stock}")

    # G. Review CRUD & Rating Recalculation
    print("-> G. Testing Review Submission & Dynamic Rating Calculation")
    review_url = reverse('add_review', kwargs={'product_id': str(prod.pk)})
    resp = client.post(review_url, {
        'rating': 5,
        'comment': 'Excellent quality, increased my yield significantly!',
        'crop_used_on': 'Wheat'
    })
    assert resp.status_code == 302
    prod.refresh_from_db()
    assert prod.rating == Decimal('5.0')
    assert prod.review_count == 1
    log(f"Review created! Product rating is now {prod.rating}★ ({prod.review_count} reviews)")

    # H. Wishlist CRUD
    print("-> H. Testing Wishlist CRUD")
    wishlist_url = reverse('toggle_wishlist', kwargs={'pk': str(prod.pk)})
    resp = client.get(wishlist_url)
    assert resp.status_code == 302
    assert Wishlist.objects.filter(user=user, product=prod).exists()
    log("Added product to Wishlist")

    resp = client.get(wishlist_url)
    assert resp.status_code == 302
    assert not Wishlist.objects.filter(user=user, product=prod).exists()
    log("Removed product from Wishlist")

    # Cleanup test items
    order.items.all().delete()
    order.delete()
    prod.reviews.all().delete()
    prod.delete()
    cat.delete()
    user.delete()
    log("Cleaned up test fixtures successfully")
    return True

def test_admin_panel(client):
    print("\n--- 4. Testing Admin Control Center ---")
    admin_user, _ = User.objects.get_or_create(
        username='test_admin_qa',
        defaults={'email': 'admin_qa@example.com', 'is_staff': True, 'is_superuser': True}
    )
    admin_user.set_password('AdminPass123!')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    client.force_login(admin_user)

    admin_urls = [
        ('/admin-panel/', "Admin Dashboard Overview"),
        ('/admin-panel/products/', "Admin Products Inventory"),
        ('/admin-panel/products/add/', "Admin Add Product Form"),
        ('/admin-panel/orders/', "Admin Orders Management"),
        ('/admin-panel/categories/', "Admin Categories Management"),
        ('/admin-panel/customers/', "Admin Customers List"),
        ('/admin-panel/reviews/', "Admin Reviews Moderation"),
        ('/admin-panel/announcements/', "Admin Announcements Control"),
    ]

    all_passed = True
    for url, desc in admin_urls:
        resp = client.get(url)
        if resp.status_code == 200:
            log(f"Admin GET {url} [{desc}] -> HTTP 200")
        else:
            log(f"Admin GET {url} [{desc}] -> Expected 200, got {resp.status_code}", success=False)
            all_passed = False

    admin_user.delete()
    log("Admin panel verification completed & clean")
    return all_passed

if __name__ == '__main__':
    print("=====================================================")
    print("  FarmKart Full System & CRUD Verification Suite     ")
    print("=====================================================")
    client = Client()
    t_ok = test_template_compilation()
    p_ok = test_public_pages_and_api(client)
    c_ok = test_crud_operations(client)
    a_ok = test_admin_panel(client)

    print("\n=====================================================")
    if t_ok and p_ok and c_ok and a_ok:
        print("🎉 ALL TESTS PASSED! 100% ERROR-FREE VERIFICATION!")
        sys.exit(0)
    else:
        print("⚠️ SOME TESTS FAILED. PLEASE CHECK OUTPUT ABOVE.")
        sys.exit(1)
