# Step 1: Create an AdminSite subclass in adminLogs/admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.models import LogEntry
from .models import AdminActivity
from dashboard.models import weatherStation  



class BlitzAgroTechAdminSite(admin.AdminSite):
    # Customize site branding
    site_header = "BlitzAgroTech Admin"
    site_title = "BlitzAgroTech Admin Portal"
    index_title = "Welcome to BlitzAgroTech Admin"
    
    # Customize default login template
    login_template = 'custom_login.html'
    
    # Optional: Custom index dashboard
    index_template = 'custom_index.html'

# Create an instance of our custom admin site
admin_site = BlitzAgroTechAdminSite(name='blitzadmin')

# Step 2: Create a custom admin model for AdminActivity
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ('admin', 'activity_type', 'description', 'timestamp')
    list_filter = ('activity_type', 'timestamp', 'admin')
    search_fields = ('description', 'admin__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('admin', 'activity_type', 'description', 'timestamp')
    
    def has_add_permission(self, request):
        return False  # Cannot manually add logs
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete logs

# Step 3: Custom user admin to fit your needs
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    actions = ['activate_users', 'deactivate_users']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    def activate_users(self, request, queryset):
        # Log admin action before making changes
        for user in queryset:
            if not user.is_active:
                AdminActivity.objects.create(
                    admin=request.user,
                    activity_type="User Activation",
                    description=f"Activated user: {user.username}"
                )
        
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} users were successfully activated.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        # Log admin action before making changes
        for user in queryset:
            if user.is_active:
                AdminActivity.objects.create(
                    admin=request.user,
                    activity_type="User Deactivation",
                    description=f"Deactivated user: {user.username}"
                )
        
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} users were successfully deactivated.")
    deactivate_users.short_description = "Deactivate selected users"

# Step 4: Register models with our custom admin site
admin_site.register(AdminActivity, AdminActivityAdmin)
admin_site.register(User, CustomUserAdmin)
admin_site.register(Group)  # Register the built-in Group model
admin_site.register(LogEntry)  # Optionally register Django's built-in LogEntry model

# Step 5: Register other models here as needed
# admin_site.register(WeatherStation, WeatherStationAdmin)
class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'city_name', 'latitude', 'longitude')
    list_filter = ('is_active',)
    search_fields = ('station_name', 'city_name', 'id')
    
admin_site.register(weatherStation, WeatherStationAdmin)
