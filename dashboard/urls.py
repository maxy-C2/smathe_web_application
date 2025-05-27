from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from . import views
from .views import ChartData, WeatherUpdate

urlpatterns = [
    # Authentication URLs
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    

    # Dashboard URLs
    path('user_menu/', views.user_menu, name='user_menu'),
    path('contact/', views.contact, name='contact'),
    path('weather_updates/', views.weather_updates, name='weather_updates'),
    path('stations_interface/', views.Stations_Interface, name='stations_interface'),
    
    # API URLs
    re_path(r'^$', ChartData.as_view(), name='home'),
    re_path(r'^api/data/$', csrf_exempt(WeatherUpdate.as_view()), name='api-data'),
    re_path(r'^bar-graph/$', ChartData.as_view(), name='bar-graph'),
]