from django.db import models
from django.contrib.auth.models import User


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