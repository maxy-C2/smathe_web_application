from django.urls import include, re_path, path
from django.views.decorators.csrf import csrf_exempt
from .views import ChartData, WeatherUpdate, Stations_Interface # weatherdataView,

urlpatterns = [
    re_path(r'^$', ChartData.as_view(), name='home'),
    re_path(r'^api/data/$', csrf_exempt(WeatherUpdate.as_view()), name='api-data'),
    re_path(r'^bar-graph$', ChartData.as_view(), name='bar-graph'),
    path('stations_interface/', Stations_Interface, name="stations_interface")

]
