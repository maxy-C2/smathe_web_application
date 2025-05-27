from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
import csv

# Import your models
from .models import AdminActivity
from dashboard.models import weatherStation, weatherData

# Helper functions
def staff_check(user):
    """Check if the user is staff"""
    return user.is_authenticated and user.is_staff

def admin_check(user):
    """Check if the user is admin/superuser"""
    return user.is_authenticated and user.is_superuser

# Authentication views
def admin_login(request):
    """Custom login view for admin users"""
    # If user already authenticated, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            # Log admin login activity
            AdminActivity.objects.create(
                admin=user,
                activity_type="Login",
                description=f"Admin login from {request.META.get('REMOTE_ADDR', '0.0.0.0')}"
            )
            # Redirect to next URL if provided, otherwise dashboard
            next_url = request.GET.get('next', 'admin_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid login credentials or insufficient permissions")
    
    return render(request, 'adminLogs/login.html', {'title': 'Admin Login'})

@login_required
def admin_logout(request):
    """Handle admin logout"""
    if request.user.is_authenticated and request.user.is_staff:
        # Log admin logout activity
        AdminActivity.objects.create(
            admin=request.user,
            activity_type="Logout",
            description=f"Admin logout from {request.META.get('REMOTE_ADDR', '0.0.0.0')}"
        )
    
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('admin_login')

def admin_forgot_password(request):
    """Handle admin password reset requests"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_staff=True)
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send reset email
            reset_link = f"{request.scheme}://{request.get_host()}/adminLogs/reset/{uid}/{token}/"
            email_subject = 'Password Reset Request - BlitzAgroTech Admin'
            email_message = f"""
            Hello {user.username},
            
            You've requested a password reset for your BlitzAgroTech admin account.
            Please click the link below to reset your password:
            
            {reset_link}
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            BlitzAgroTech Team
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
            
            messages.success(request, "Password reset instructions have been sent to your email")
            return redirect('admin_password_reset_done')
        except User.DoesNotExist:
            # Don't reveal which emails exist in our system
            messages.success(request, "If your email exists in our system, you will receive reset instructions")
            return redirect('admin_password_reset_done')
    
    return render(request, 'adminLogs/forgot_password.html', {'title': 'Forgot Password'})

def admin_password_reset_done(request):
    """Show confirmation page after password reset request"""
    return render(request, 'adminLogs/password_reset_done.html', {'title': 'Password Reset Sent'})

def admin_password_reset_confirm(request, uidb64, token):
    """Handle password reset confirmation"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid, is_staff=True)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Check if the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, "Passwords don't match")
                return render(request, 'adminLogs/password_reset_confirm.html', {
                    'validlink': True,
                    'title': 'Reset Password'
                })
            
            # Set new password
            user.set_password(password1)
            user.save()
            
            # Log password change
            AdminActivity.objects.create(
                admin=user,
                activity_type="Password Reset",
                description=f"Password reset via email link"
            )
            
            messages.success(request, "Password has been reset successfully. You can now login with your new password.")
            return redirect('admin_login')
        
        return render(request, 'adminLogs/password_reset_confirm.html', {
            'validlink': True,
            'title': 'Reset Password'
        })
    else:
        return render(request, 'adminLogs/password_reset_confirm.html', {
            'validlink': False,
            'title': 'Reset Password'
        })

# Dashboard views
@login_required
@user_passes_test(staff_check)
def admin_dashboard(request):
    """Admin dashboard with overview stats"""
    # Get basic stats
    total_users = User.objects.count()
    total_weather_stations = weatherStation.objects.count()
    total_data_points = weatherData.objects.count()
    recent_activities = AdminActivity.objects.all()[:10]
    
    # Get user registration stats for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users_by_day = (
        User.objects.filter(date_joined__gte=thirty_days_ago)
        .extra({'day': "date(date_joined)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    
    # Get weather data stats (last 24 hours)
    last_day = timezone.now() - timedelta(hours=24)
    hourly_data = (
        weatherData.objects.filter(created__gte=last_day)
        .extra({'hour': "date_trunc('hour', created)"})
        .values('hour')
        .annotate(
            avg_temp=Avg('airTemperature'),
            avg_humidity=Avg('relativeHumidity')
        )
        .order_by('hour')
    )
    
    # Prepare chart data
    user_chart_data = {
        'labels': [entry['day'].strftime('%b %d') for entry in new_users_by_day],
        'data': [entry['count'] for entry in new_users_by_day]
    }
    
    weather_chart_data = {
        'labels': [entry['hour'].strftime('%H:%M') for entry in hourly_data],
        'temp_data': [float(entry['avg_temp'] or 0) for entry in hourly_data],
        'humidity_data': [float(entry['avg_humidity'] or 0) for entry in hourly_data]
    }
    
    # Format for template
    context = {
        'title': 'Admin Dashboard',
        'total_users': total_users,
        'total_weather_stations': total_weather_stations,
        'total_data_points': total_data_points,
        'recent_activities': recent_activities,
        'user_chart_data': json.dumps(user_chart_data),
        'weather_chart_data': json.dumps(weather_chart_data)
    }
    
    return render(request, 'adminLogs/dashboard.html', context)

# User management views
@login_required
@user_passes_test(staff_check)
def manage_users(request):
    """View and manage users"""
    # Handle search and filtering
    search_query = request.GET.get('search', '')
    user_filter = request.GET.get('filter', 'all')
    
    # Base queryset
    users = User.objects.all().order_by('-date_joined')
    
    # Apply search if provided
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Apply filters
    if user_filter == 'staff':
        users = users.filter(is_staff=True)
    elif user_filter == 'active':
        users = users.filter(is_active=True)
    elif user_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(users, 20)  # 20 users per page
    page_number = request.GET.get('page', 1)
    users_page = paginator.get_page(page_number)
    
    context = {
        'title': 'Manage Users',
        'users': users_page,
        'search_query': search_query,
        'user_filter': user_filter,
        'user_count': users.count()
    }
    
    return render(request, 'adminLogs/manage_users.html', context)

@login_required
@user_passes_test(staff_check)
def edit_user(request, user_id):
    """Edit user details"""
    user = get_object_or_404(User, pk=user_id)
    
    # Check permissions - only superusers can edit other superusers
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this user")
        return redirect('manage_users')
    
    if request.method == 'POST':
        # Update user details
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        # Staff and superuser status (only superusers can change these)
        if request.user.is_superuser:
            user.is_staff = 'is_staff' in request.POST
            user.is_superuser = 'is_superuser' in request.POST
        
        # Set new password if provided
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        
        user.save()
        
        # Log the activity
        AdminActivity.objects.create(
            admin=request.user,
            activity_type="User Update",
            description=f"Updated user: {user.username}"
        )
        
        messages.success(request, f"User {user.username} has been updated successfully")
        return redirect('manage_users')
    
    context = {
        'title': f'Edit User: {user.username}',
        'user_obj': user
    }
    
    return render(request, 'adminLogs/edit_user.html', context)

@login_required
@user_passes_test(staff_check)
def activate_user(request, user_id):
    """Activate a user account"""
    user = get_object_or_404(User, pk=user_id)
    
    # Check permissions
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "You don't have permission to modify this user")
        return redirect('manage_users')
    
    user.is_active = True
    user.save()
    
    # Log the activity
    AdminActivity.objects.create(
        admin=request.user,
        activity_type="User Activation",
        description=f"Activated user account: {user.username}"
    )
    
    messages.success(request, f"User {user.username} has been activated")
    return redirect('manage_users')

@login_required
@user_passes_test(staff_check)
def deactivate_user(request, user_id):
    """Deactivate a user account"""
    user = get_object_or_404(User, pk=user_id)
    
    # Check permissions
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "You don't have permission to modify this user")
        return redirect('manage_users')
    
    # Prevent self-deactivation
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account")
        return redirect('manage_users')
    
    user.is_active = False
    user.save()
    
    # Log the activity
    AdminActivity.objects.create(
        admin=request.user,
        activity_type="User Deactivation",
        description=f"Deactivated user account: {user.username}"
    )
    
    messages.success(request, f"User {user.username} has been deactivated")
    return redirect('manage_users')

@login_required
@user_passes_test(admin_check)
def delete_user(request, user_id):
    """Delete a user account (superuser only)"""
    user = get_object_or_404(User, pk=user_id)
    
    # Prevent self-deletion
    if user == request.user:
        messages.error(request, "You cannot delete your own account")
        return redirect('manage_users')
    
    username = user.username
    user.delete()
    
    # Log the activity
    AdminActivity.objects.create(
        admin=request.user,
        activity_type="User Deletion",
        description=f"Deleted user account: {username}"
    )
    
    messages.success(request, f"User {username} has been deleted")
    return redirect('manage_users')

# Weather station management
@login_required
@user_passes_test(staff_check)
def manage_weather_stations(request):
    """View and manage weather stations"""
    stations = weatherStation.objects.all().order_by('station_name')
    
    # Handle adding new stations
    if request.method == 'POST':
        station_name = request.POST.get('station_name')
        city_name = request.POST.get('city_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Basic validation
        if not all([station_name, city_name, latitude, longitude]):
            messages.error(request, "All fields are required")
        else:
            try:
                # Create new weather station
                station = weatherStation.objects.create(
                    station_name=station_name,
                    city_name=city_name,
                    latitude=latitude,
                    longitude=longitude
                )
                
                # Log the activity
                AdminActivity.objects.create(
                    admin=request.user,
                    activity_type="Weather Station Addition",
                    description=f"Added new weather station: {station_name} in {city_name}"
                )
                
                messages.success(request, f"Weather station '{station_name}' has been added successfully")
                return redirect('manage_weather_stations')
            except Exception as e:
                messages.error(request, f"Error adding weather station: {str(e)}")
    
    context = {
        'title': 'Manage Weather Stations',
        'stations': stations
    }
    
    return render(request, 'adminLogs/manage_weather_stations.html', context)

@login_required
@user_passes_test(staff_check)
def edit_weather_station(request, station_id):
    """Edit weather station details"""
    station = get_object_or_404(weatherStation, pk=station_id)
    
    if request.method == 'POST':
        station.station_name = request.POST.get('station_name', station.station_name)
        station.city_name = request.POST.get('city_name', station.city_name)
        station.latitude = request.POST.get('latitude', station.latitude)
        station.longitude = request.POST.get('longitude', station.longitude)
        
        # Check if there's an is_active field
        try:
            station.is_active = 'is_active' in request.POST
        except AttributeError:
            # Field doesn't exist, ignore
            pass
            
        station.save()
        
        # Log the activity
        AdminActivity.objects.create(
            admin=request.user,
            activity_type="Weather Station Update",
            description=f"Updated weather station: {station.station_name}"
        )
        
        messages.success(request, f"Weather station '{station.station_name}' has been updated")
        return redirect('manage_weather_stations')
    
    context = {
        'title': f'Edit Weather Station: {station.station_name}',
        'station': station
    }
    
    return render(request, 'adminLogs/edit_weather_station.html', context)

@login_required
@user_passes_test(admin_check)
def delete_weather_station(request, station_id):
    """Delete a weather station (superuser only)"""
    station = get_object_or_404(weatherStation, pk=station_id)
    station_name = station.station_name
    
    station.delete()
    
    # Log the activity
    AdminActivity.objects.create(
        admin=request.user,
        activity_type="Weather Station Deletion",
        description=f"Deleted weather station: {station_name}"
    )
    
    messages.success(request, f"Weather station '{station_name}' has been deleted")
    return redirect('manage_weather_stations')

# System logs and settings
@login_required
@user_passes_test(staff_check)
def system_logs(request):
    """View system logs and admin activity"""
    # Get filter parameters
    activity_type = request.GET.get('activity_type', '')
    admin_filter = request.GET.get('admin', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Base queryset
    logs = AdminActivity.objects.all().order_by('-timestamp')
    
    # Apply filters
    if activity_type:
        logs = logs.filter(activity_type=activity_type)
    
    if admin_filter:
        logs = logs.filter(admin__username=admin_filter)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            logs = logs.filter(timestamp__date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            logs = logs.filter(timestamp__date__lte=date_to_obj)
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(logs, 50)  # 50 logs per page
    page_number = request.GET.get('page', 1)
    logs_page = paginator.get_page(page_number)
    
    # Get distinct activity types and admins for filters
    activity_types = AdminActivity.objects.values_list('activity_type', flat=True).distinct()
    admins = User.objects.filter(adminactivity__isnull=False).distinct()
    
    # Export to CSV if requested
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="admin_logs.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Admin', 'Activity Type', 'Description', 'Timestamp'])
        
        for log in logs:
            writer.writerow([
                log.admin.username,
                log.activity_type,
                log.description,
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    context = {
        'title': 'System Logs',
        'logs': logs_page,
        'activity_types': activity_types,
        'admins': admins,
        'filters': {
            'activity_type': activity_type,
            'admin': admin_filter,
            'date_from': date_from,
            'date_to': date_to
        }
    }
    
    return render(request, 'adminLogs/system_logs.html', context)

@login_required
@user_passes_test(admin_check)
def admin_settings(request):
    """Configure system settings (placeholder)"""
    if request.method == 'POST':
        # Process settings updates here
        messages.success(request, "Settings have been updated successfully")
        
        # Log the activity
        AdminActivity.objects.create(
            admin=request.user,
            activity_type="Settings Update",
            description="Updated system settings"
        )
    
    context = {
        'title': 'System Settings'
    }
    
    return render(request, 'adminLogs/admin_settings.html', context)

# API endpoints
@login_required
@user_passes_test(staff_check)
def log_admin_activity(request):
    """API endpoint to log admin activity"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            activity_type = data.get('activity_type', 'API Action')
            description = data.get('description', 'Admin action via API')
            
            AdminActivity.objects.create(
                admin=request.user,
                activity_type=activity_type,
                description=description
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)