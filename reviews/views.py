from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from products.models import Product
from .models import Review

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        crop_used_on = request.POST.get('crop_used_on', '').strip()

        if comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment,
                crop_used_on=crop_used_on,
                is_verified_farmer=True
            )
            messages.success(request, 'Thank you! Your farmer review has been posted.')
        else:
            messages.error(request, 'Please provide a comment for your review.')

    return redirect('product_detail', pk=product_id)
