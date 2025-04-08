from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from django.db.models import Q

from .tokens import generate_admin_token
from .models import AdminActivity
from ..smartWeatherProject import settings


# Check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser


@csrf_protect
def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None and is_admin(user):
            login(request, user)
            # Log admin login activity
            AdminActivity.objects.create(
                admin=user,
                activity_type="Login",
                description=f"Admin user {username} logged in"
            )
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")
    
    return render(request, "admin_login.html")


@login_required
def admin_logout(request):
    """Admin logout view"""
    if is_admin(request.user):
        username = request.user.username
        # Log admin logout activity
        AdminActivity.objects.create(
            admin=request.user,
            activity_type="Logout",
            description=f"Admin user {username} logged out"
        )
    logout(request)
    return redirect('admin_login')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get stats for dashboard
    user_count = User.objects.count()
    # This would be replaced with actual weather station model
    station_count = 0  # Weather station count would come from your model
    
    # New users in last 7