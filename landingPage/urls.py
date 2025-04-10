# Update your project's main urls.py file:

from django.urls import path, include
from adminLogs.admin import admin_site  # Import our custom admin site

urlpatterns = [
    # Use our custom admin site instead of the default
    path('admin/', admin_site.urls),
    
    # Other URL patterns...
]

