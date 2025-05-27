from django.contrib import admin
from .models import weatherData, weatherStation, search

admin.site.register(weatherData)
admin.site.register(weatherStation)
admin.site.register(search)