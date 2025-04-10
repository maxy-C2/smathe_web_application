# Update adminLogs/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


class AdminActivity(models.Model):
    """
    Model to track admin activities in the system
    """
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admin.username} - {self.activity_type} - {self.timestamp}"
    
    class Meta:
        verbose_name_plural = "Admin Activities"
        ordering = ['-timestamp']


@receiver(post_save, sender=LogEntry)
def log_admin_activity_from_log_entry(sender, instance, created, **kwargs):
    """
    Signal to automatically create AdminActivity records from Django's LogEntry
    """
    if created:
        # Determine the action type
        if instance.action_flag == ADDITION:
            activity_type = "Create"
        elif instance.action_flag == CHANGE:
            activity_type = "Update"
        elif instance.action_flag == DELETION:
            activity_type = "Delete"
        else:
            activity_type = "Unknown"
        
        # Create the activity log
        AdminActivity.objects.create(
            admin=instance.user,
            activity_type=activity_type,
            description=instance.change_message or f"{activity_type} {instance.content_type} {instance.object_repr}"
        )


# Optional: Custom Context Processor to add stats to admin dashboard
def admin_stats_context(request):
    """Context processor to add stats to the admin templates"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return {}
        
    # Only process for admin URLs
    if not request.path.startswith('/admin/'):
        return {}
        
    context = {
        'user_count': User.objects.count(),
        'activity_count': AdminActivity.objects.count(),
        # Add other stats as needed
    }
    
    return context