from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Wishlist

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True).order_by('-rating')[:8]
    if not featured_products.exists():
        featured_products = Product.objects.order_by('-rating')[:8]

    deals_of_the_day = Product.objects.filter(discount__gt=10).order_by('-discount')[:8]
    if not deals_of_the_day.exists():
        deals_of_the_day = Product.objects.order_by('-discount')[:8]

    organic_products = Product.objects.filter(is_organic=True)[:6]
    best_sellers = Product.objects.filter(is_best_seller=True)[:6]
    if not best_sellers.exists():
        best_sellers = Product.objects.order_by('-stock')[:6]

    # Get wished product ids for current user
    wished_ids = set()
    if request.user.is_authenticated:
        wished_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'deals_of_the_day': deals_of_the_day,
        'organic_products': organic_products,
        'best_sellers': best_sellers,
        'wished_ids': wished_ids,
    }
    return render(request, 'products/home.html', context)

def product_list(request):
    q = request.GET.get('q', '').strip()
    cat_id = request.GET.get('category', '').strip()
    sort_by = request.GET.get('sort', 'popular')
    organic = request.GET.get('organic', '')
    in_stock_only = request.GET.get('in_stock', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    products = Product.objects.all()

    # Search filter
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(brand__icontains=q) |
            Q(hindi_name__icontains=q) |
            Q(crop_type__icontains=q) |
            Q(description__icontains=q)
        )

    # Category filter
    if cat_id:
        products = products.filter(category_id=cat_id)

    # Organic filter
    if organic == '1':
        products = products.filter(is_organic=True)

    # In-stock filter
    if in_stock_only == '1':
        products = products.filter(stock__gt=0)

    # Price range
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'discount':
        products = products.order_by('-discount')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-rating', '-created_at')

    # Wished items
    wished_ids = set()
    if request.user.is_authenticated:
        wished_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    selected_category = None
    if cat_id:
        selected_category = Category.objects.filter(id=cat_id).first()

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'selected_category': selected_category,
        'q': q,
        'cat_id': cat_id,
        'sort_by': sort_by,
        'organic': organic,
        'in_stock_only': in_stock_only,
        'min_price': min_price,
        'max_price': max_price,
        'total_count': products.count(),
        'wished_ids': wished_ids,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wished = request.user.is_authenticated and Wishlist.objects.filter(user=request.user, product=product).exists()
    reviews = product.reviews.all().order_by('-created_at')

    # Related / similar products in same category
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]

    wished_ids = set()
    if request.user.is_authenticated:
        wished_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'product': product,
        'wished': wished,
        'reviews': reviews,
        'related_products': related_products,
        'wished_ids': wished_ids,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item = Wishlist.objects.filter(user=request.user, product=product).first()
    next_url = request.GET.get('next')

    if item:
        item.delete()
        messages.info(request, f'Removed {product.name} from your wishlist.')
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f'Added {product.name} to your wishlist!')

    if next_url:
        return redirect(next_url)
    return redirect('product_detail', pk=pk)

@login_required
def my_wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'products/my_wishlist.html', {'wishlist_items': items})

def agri_calculator(request):
    """Kisan Fertilizer Dosage & Crop Advisory Calculator Tool."""
    crop = request.GET.get('crop', 'wheat')
    try:
        acres = float(request.GET.get('acres', 1))
        if acres <= 0:
            acres = 1.0
    except ValueError:
        acres = 1.0

    crop_guidelines = {
        'wheat': {
            'name': 'Wheat (गेहूं)',
            'season': 'Rabi (रबी)',
            'urea_per_acre': 2.5,
            'dap_per_acre': 1.0,
            'mop_per_acre': 0.5,
            'zinc_per_acre': 5,
            'search_term': 'Wheat',
            'stages': [
                'Basal Dose (बुवाई के समय): 1 Bag DAP + 0.5 Bag MOP + 1 Bag Urea',
                'Crown Root Initiation (CRI Stage - 21 Days): 1 Bag Urea + 5 kg Zinc Sulfate',
                'Booting & Flowering Stage: 0.5 Bag Urea or 19-19-19 Foliar Spray'
            ]
        },
        'paddy': {
            'name': 'Paddy / Rice (धान)',
            'season': 'Kharif (खरीफ)',
            'urea_per_acre': 2.7,
            'dap_per_acre': 1.2,
            'mop_per_acre': 0.6,
            'zinc_per_acre': 7,
            'search_term': 'Rice',
            'stages': [
                'Transplanting (रोपाई): Full DAP (1.2 Bags) + 0.6 Bag MOP + 1 Bag Urea',
                'Active Tillering (25-30 Days): 1 Bag Urea + Micronutrient Zinc Spray',
                'Panicle Initiation (50 Days): 0.7 Bag Urea'
            ]
        },
        'cotton': {
            'name': 'Cotton (कपास)',
            'season': 'Kharif (खरीफ)',
            'urea_per_acre': 3.0,
            'dap_per_acre': 1.5,
            'mop_per_acre': 1.0,
            'zinc_per_acre': 6,
            'search_term': 'Cotton',
            'stages': [
                'Basal: 1.5 Bags DAP + 1 Bag MOP + 0.5 Bag Urea',
                'Square Formation: 1.2 Bags Urea + Boron / Magnesium Spray',
                'Boll Development: 1.3 Bags Urea + 00-52-34 Spray'
            ]
        },
        'sugarcane': {
            'name': 'Sugarcane (गन्ना)',
            'season': 'Annual (सालाना)',
            'urea_per_acre': 5.0,
            'dap_per_acre': 2.0,
            'mop_per_acre': 1.5,
            'zinc_per_acre': 10,
            'search_term': 'Sugarcane',
            'stages': [
                'Planting (बुवाई): 2 Bags DAP + 1.5 Bags MOP + 1.5 Bags Urea',
                'Formative Stage (60-90 Days): 2 Bags Urea',
                'Grand Growth Phase: 1.5 Bags Urea + Bio-Fertilizer Soil Drench'
            ]
        },
        'potato': {
            'name': 'Potato (आलू)',
            'season': 'Rabi (रबी)',
            'urea_per_acre': 3.5,
            'dap_per_acre': 2.0,
            'mop_per_acre': 1.8,
            'zinc_per_acre': 8,
            'search_term': 'Potato',
            'stages': [
                'Planting: Full DAP (2 Bags) + Full MOP (1.8 Bags) + 1.5 Bags Urea',
                'Earthing Up (30 Days): 2 Bags Urea + Water Soluble NPK 19-19-19'
            ]
        },
        'mustard': {
            'name': 'Mustard (सरसों)',
            'season': 'Rabi (रबी)',
            'urea_per_acre': 2.0,
            'dap_per_acre': 1.0,
            'mop_per_acre': 0.4,
            'zinc_per_acre': 5,
            'search_term': 'Mustard',
            'stages': [
                'Basal: 1 Bag DAP + 0.4 Bag MOP + 1 Bag Urea + 10 kg Sulphur',
                'Flowering (35-40 Days): 1 Bag Urea'
            ]
        },
        'vegetables': {
            'name': 'Vegetables & Tomato (सब्जियां व टमाटर)',
            'season': 'Multi-Season',
            'urea_per_acre': 2.2,
            'dap_per_acre': 1.5,
            'mop_per_acre': 1.0,
            'zinc_per_acre': 5,
            'search_term': 'Vegetables',
            'stages': [
                'Transplanting: 1.5 Bags DAP + 1 Bag MOP + 0.7 Bag Urea',
                'Vegetative Growth: 0.8 Bag Urea + Humic Acid + Micronutrients',
                'Fruiting / Picking: 0.7 Bag Urea + 13-0-45 Potash Foliar Spray'
            ]
        }
    }

    selected = crop_guidelines.get(crop, crop_guidelines['wheat'])

    calc_result = {
        'crop_name': selected['name'],
        'season': selected['season'],
        'acres': acres,
        'urea_bags': round(selected['urea_per_acre'] * acres, 1),
        'dap_bags': round(selected['dap_per_acre'] * acres, 1),
        'mop_bags': round(selected['mop_per_acre'] * acres, 1),
        'zinc_kg': round(selected['zinc_per_acre'] * acres, 1),
        'stages': selected['stages'],
    }

    # Recommended matching products from catalog
    recommended_products = Product.objects.filter(
        Q(name__icontains='NPK') |
        Q(name__icontains='Fertilizer') |
        Q(name__icontains='Seed') |
        Q(crop_type__icontains=selected['search_term']) |
        Q(category__name__icontains='Fertilizer') |
        Q(is_organic=True)
    ).distinct()[:6]

    context = {
        'crops': crop_guidelines,
        'selected_crop': crop,
        'acres': acres,
        'result': calc_result,
        'recommended_products': recommended_products,
    }
    return render(request, 'products/calculator.html', context)

