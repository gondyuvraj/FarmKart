from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty. Add products to continue.')
        return redirect('cart')

    products = []
    items_total = Decimal('0')
    mrp_total = Decimal('0')

    for sid, qty in cart.items():
        try:
            p = Product.objects.get(pk=sid)
            subtotal = p.sale_price * qty
            mrp_subtotal = p.price * qty
            products.append((p, qty, subtotal))
            items_total += subtotal
            mrp_total += mrp_subtotal
        except Product.DoesNotExist:
            continue

    savings_total = mrp_total - items_total
    delivery_fee = Decimal('0') if items_total >= Decimal('999') else Decimal('49')
    final_total = items_total + delivery_fee

    if request.method == 'POST' and products:
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        landmark = request.POST.get('landmark', '').strip()
        payment_method = request.POST.get('payment_method', 'COD')
        notes = request.POST.get('notes', '').strip()

        if not (name and phone and address and city and pincode):
            messages.error(request, 'Please fill in all mandatory delivery address fields.')
            return render(request, 'orders/checkout.html', {
                'items': products,
                'items_total': items_total,
                'mrp_total': mrp_total,
                'savings_total': savings_total,
                'delivery_fee': delivery_fee,
                'final_total': final_total,
            })

        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            landmark=landmark,
            total=final_total,
            payment_method=payment_method,
            payment_status='PAID' if payment_method == 'UPI' else 'PENDING',
            notes=notes,
            status='CONFIRMED' if payment_method == 'COD' else 'PLACED',
            expected_delivery='2 - 4 Business Days'
        )

        for p, q, s in products:
            OrderItem.objects.create(order=order, product=p, quantity=q, price=p.sale_price)
            p.stock = max(0, p.stock - q)
            p.save()

        # Clear session cart
        request.session['cart'] = {}
        messages.success(request, f'Order placed successfully! Order ID: {order.order_number}')
        return redirect('order_success', pk=str(order.id))

    return render(request, 'orders/checkout.html', {
        'items': products,
        'items_total': items_total,
        'mrp_total': mrp_total,
        'savings_total': savings_total,
        'delivery_fee': delivery_fee,
        'final_total': final_total,
    })

@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_invoice(request, pk):
    """Printable GST/Kisan invoice receipt for customer or staff."""
    if request.user.is_staff or request.user.is_superuser:
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_invoice.html', {'order': order})

@login_required
def cancel_order(request, pk):
    """Customer self-service order cancellation before dispatch."""
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status in ['PLACED', 'CONFIRMED']:
            # Restore stock for each item in the cancelled order
            for item in order.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save(update_fields=['stock'])
            order.status = 'CANCELLED'
            order.save(update_fields=['status'])
            messages.success(request, f'Order #{order.order_number} has been cancelled successfully. Any pending payment will not be charged.')
        else:
            messages.error(request, f'Order #{order.order_number} cannot be cancelled as it is already in transit or delivered.')
    return redirect('order_detail', pk=pk)

