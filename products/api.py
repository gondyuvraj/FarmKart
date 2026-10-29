from django.http import JsonResponse
from .models import Product

def product_api(request):
    data = [
        {
            'id': str(p.id),
            'name': p.name,
            'hindi_name': p.hindi_name,
            'brand': p.brand,
            'category': p.category.name if p.category else None,
            'price': float(p.price),
            'discount': float(p.discount),
            'sale_price': float(p.sale_price),
            'unit': p.unit,
            'stock': p.stock,
            'crop_type': p.crop_type,
            'dosage': p.dosage,
            'is_organic': p.is_organic,
            'rating': float(p.rating),
            'review_count': p.review_count,
            'image_url': request.build_absolute_uri(p.image.url) if p.image else None,
        }
        for p in Product.objects.select_related('category')
    ]
    return JsonResponse({'status': 'success', 'count': len(data), 'products': data}, safe=False)
