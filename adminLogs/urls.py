from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('forgot-password/', views.admin_forgot_password, name='admin_forgot_password'),
    path('password-reset-done/', views.admin_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.admin_password_reset_confirm, name='password_reset_confirm'),
    
    # Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User management
    path('users/', views.manage_users, name='manage_users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('users/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Weather station management
    path('weather-stations/', views.manage_weather_stations, name='manage_weather_stations'),
    path('weather-stations/edit/<int:station_id>/', views.edit_weather_station, name='edit_weather_station'),
    path('weather-stations/delete/<int:station_id>/', views.delete_weather_station, name='delete_weather_station'),
    
    # System logs and settings
    path('system-logs/', views.system_logs, name='system_logs'),
    path('settings/', views.admin_settings, name='admin_settings'),
    
    # API endpoints
    path('api/log-activity/', views.log_admin_activity, name='log_admin_activity'),
]