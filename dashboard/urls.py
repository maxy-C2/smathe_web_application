from django.urls import path
from . import views

urlpatterns = [
    path('user_menu', views.user_menu, name='user_menu'),
    path('weather_updates', views.weather_updates, name='weather_updates'),
    path('contact', views.contact, name='contact'),


]
