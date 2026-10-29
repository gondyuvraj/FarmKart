from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from orders.models import Order
from products.models import Wishlist
from .models import UserProfile

def register(request):
    """Farmer Account Registration with crop profile and contact details."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        username = request.POST.get('username', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        state = request.POST.get('state', 'Maharashtra').strip()
        district = request.POST.get('district', '').strip()
        primary_crop = request.POST.get('primary_crop', 'Wheat').strip()
        land_size = request.POST.get('land_size', '2 - 5 Acres').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match. Please re-enter.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken. Please pick another.')
        else:
            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name
            )

            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                phone=phone,
                state=state,
                district=district,
                primary_crop=primary_crop,
                land_size=land_size,
                is_verified_farmer=True
            )

            login(request, user)
            messages.success(request, f'Namaste {user.first_name or user.username}! Your FarmKart Kisan account has been created.')
            return redirect('home')

    return render(request, 'accounts/register.html')


def login_view(request):
    """Dual-Role Login View: Farmer / Customer and Admin Control Center."""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home')

    active_tab = request.GET.get('role', 'user')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        login_role = request.POST.get('login_role', 'user')
        remember_me = request.POST.get('remember_me') == '1'
        next_url = request.GET.get('next', '').strip()

        user = authenticate(request, username=username, password=password)

        if user:
            # Handle Remember Me Session Expiry
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser close

            login(request, user)

            # Role-Specific Redirection & Verification
            if login_role == 'admin':
                if user.is_staff or user.is_superuser:
                    messages.success(request, f'Welcome back, {user.first_name or user.username}! Logged in as Administrator.')
                    return redirect('admin_dashboard')
                else:
                    messages.warning(
                        request,
                        f'Logged in as {user.username}. Note: This account does not have Admin privileges. Redirected to customer storefront.'
                    )
                    return redirect('home')
            else:
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                if next_url:
                    return redirect(next_url)
                if user.is_staff and not next_url:
                    return redirect('home')
                return redirect('home')

        messages.error(request, 'Invalid username or password. Please verify your credentials.')

    return render(request, 'accounts/login.html', {'active_tab': active_tab})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """Farmer Profile, Address Book, and Crop Preferences."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        state = request.POST.get('state', '').strip()
        district = request.POST.get('district', '').strip()
        primary_crop = request.POST.get('primary_crop', '').strip()
        land_size = request.POST.get('land_size', '').strip()

        request.user.first_name = first_name
        request.user.email = email
        request.user.save(update_fields=['first_name', 'email'])

        profile.phone = phone
        profile.state = state
        profile.district = district
        profile.primary_crop = primary_crop
        profile.land_size = land_size
        profile.save()

        messages.success(request, 'Your Kisan profile details have been saved successfully!')
        return redirect('profile')

    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_orders = Order.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        'profile': profile,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'accounts/profile.html', context)
