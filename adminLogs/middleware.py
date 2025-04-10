# Create a file: adminLogs/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.contrib.auth.models import User
from .models import AdminActivity

class AdminActivityMiddleware(MiddlewareMixin):
    """
    Middleware to log admin activities automatically
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        """Process view is called before the view is actually called"""
        # Only process for authenticated staff users
        if not request.user.is_authenticated or not request.user.is_staff:
            return None
            
        # Get the URL name
        try:
            url_name = resolve(request.path_info).url_name
        except:
            url_name = None
            
        # Check if this is an admin action we want to log
        if url_name and url_name.startswith('admin:') and request.method == 'POST':
            # Determine what type of action this is
            action_type = "Unknown"
            description = f"Admin action: {url_name}"
            
            if 'delete' in url_name:
                action_type = "Delete"
                model_name = url_name.split('_')[1]
                description = f"Deleted {model_name} objects"
            elif 'add' in url_name:
                action_type = "Create"
                model_name = url_name.split('_')[1]
                description = f"Created new {model_name}"
            elif 'change' in url_name:
                action_type = "Update"
                model_name = url_name.split('_')[1]
                description = f"Updated {model_name} objects"
                
            # Log the activity
            AdminActivity.objects.create(
                admin=request.user,
                activity_type=action_type,
                description=description
            )
            
        return None