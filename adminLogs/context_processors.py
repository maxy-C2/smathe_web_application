# Create adminLogs/context_processors.py
from django.contrib.auth.models import User
from .models import AdminActivity

def admin_stats_context(request):
    """Add statistics to admin context"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return {}
        
    # Only process for admin URLs
    if not request.path.startswith('/admin/'):
        return {}
        
    context = {
        'user_count': User.objects.count(),
        'activity_count': AdminActivity.objects.filter().count(),
        'recent_activities': AdminActivity.objects.all()[:5],
        # Add other stats as needed
    }
    
    return context