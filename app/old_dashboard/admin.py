from django.contrib import admin
from .models import weatherdata

#new
from .models import Station
admin.site.register(Station)
#new



admin.site.register(weatherdata)