from products.models import Category, Wishlist

def farmkart_globals(request):
    """Global context available across all templates."""
    # Cart count
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if isinstance(cart, dict) else 0

    # Wishlist count
    wishlist_count = 0
    if request.user.is_authenticated:
        try:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        except Exception:
            wishlist_count = 0

    # Categories for navigation
    try:
        categories_nav = Category.objects.all()[:10]
    except Exception:
        categories_nav = []

    # Store dynamic announcement
    try:
        from admin_panel.views import get_announcement_data
        store_announcement = get_announcement_data()
    except Exception:
        store_announcement = {}

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'categories_nav': categories_nav,
        'store_announcement': store_announcement,
        'kisan_helpline': '1800-180-1551 (Toll-Free Kisan Call Center)',
    }
