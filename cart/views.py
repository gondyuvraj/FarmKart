from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from products.models import Product

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    items_total = Decimal('0')
    mrp_total = Decimal('0')

    for sid, qty in list(cart.items()):
        try:
            p = Product.objects.get(pk=sid)
            # Ensure quantity doesn't exceed stock
            if p.stock <= 0:
                cart.pop(sid, None)
                request.session['cart'] = cart
                continue
            qty = min(qty, p.stock)
            subtotal = p.sale_price * qty
            mrp_subtotal = p.price * qty
            items.append({
                'product': p,
                'qty': qty,
                'subtotal': subtotal,
                'mrp_subtotal': mrp_subtotal,
                'saved': mrp_subtotal - subtotal,
            })
            items_total += subtotal
            mrp_total += mrp_subtotal
        except Product.DoesNotExist:
            cart.pop(sid, None)
            request.session['cart'] = cart

    savings_total = mrp_total - items_total
    free_delivery_threshold = Decimal('999')
    delivery_fee = Decimal('0') if items_total >= free_delivery_threshold or not items else Decimal('49')
    final_total = items_total + delivery_fee
    amount_needed_for_free_delivery = max(Decimal('0'), free_delivery_threshold - items_total)

    context = {
        'items': items,
        'items_total': items_total,
        'mrp_total': mrp_total,
        'savings_total': savings_total,
        'delivery_fee': delivery_fee,
        'final_total': final_total,
        'amount_needed_for_free_delivery': amount_needed_for_free_delivery,
        'free_delivery_threshold': free_delivery_threshold,
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if p.stock <= 0:
        messages.error(request, f'Sorry, {p.name} is currently out of stock.')
        return redirect('product_detail', pk=pk)

    cart = request.session.get('cart', {})
    key = str(pk)
    add_qty = int(request.POST.get('quantity', 1))
    current_qty = cart.get(key, 0)
    new_qty = min(current_qty + add_qty, p.stock)
    cart[key] = new_qty
    request.session['cart'] = cart
    messages.success(request, f'Added {p.name} ({new_qty} in cart).')

    if request.POST.get('buy_now') == '1':
        return redirect('checkout')
    return redirect('cart')

def update_cart(request, pk):
    cart = request.session.get('cart', {})
    key = str(pk)
    action = request.POST.get('action')
    p = get_object_or_404(Product, pk=pk)

    if action == 'increase':
        qty = cart.get(key, 1) + 1
    elif action == 'decrease':
        qty = cart.get(key, 1) - 1
    else:
        qty = int(request.POST.get('quantity', 1))

    if qty <= 0:
        cart.pop(key, None)
        messages.info(request, f'Removed {p.name} from your cart.')
    else:
        qty = min(qty, p.stock)
        cart[key] = qty
        messages.info(request, f'Updated {p.name} quantity to {qty}.')

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    p = Product.objects.filter(pk=pk).first()
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    name = p.name if p else 'Item'
    messages.info(request, f'Removed {name} from your cart.')
    return redirect('cart')
