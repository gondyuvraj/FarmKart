from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """Decorator to require that the authenticated user is a staff member or superuser.
    Non-admin regular users are redirected to the homepage with an access warning."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in with administrator credentials to access the Admin Control Center.')
            return redirect(f"/accounts/login/?next={request.path}")
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Access Denied: This area is strictly reserved for FarmKart administrators.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
