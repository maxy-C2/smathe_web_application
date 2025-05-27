import json
import folium
import pandas as pd
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import weatherData, weatherStation
from .serializers import weatherSerializer
from django.contrib.auth.decorators import login_required




def get_weather_data():
    """Helper function to get weather data from database"""
    item = weatherData.objects.all().values()
    df = pd.DataFrame(item)
    
    context = {}
    if not df.empty:
        # Handle potential field name differences between model and views
        context = {
            'humidity': df['relativeHumidity'].tolist() if 'relativeHumidity' in df.columns else [],
            'temperature': df['airTemperature'].tolist() if 'airTemperature' in df.columns else [],
            'windDirection': df['windDirection'].tolist() if 'windDirection' in df.columns else [],
            'windSpeed': df['windSpeed'].tolist() if 'windSpeed' in df.columns else [],
            'rainfall': df['rainfall'].tolist() if 'rainfall' in df.columns else [],
            'soilmoisture': df['soilMoisture'].tolist() if 'soilMoisture' in df.columns else [],
            'soiltemperature': df['soilTemperature'].tolist() if 'soilTemperature' in df.columns else [],
            'lightintensity': df['lightIntensity'].tolist() if 'lightIntensity' in df.columns else [],
            'solarradiance': df['solarRadiance'].tolist() if 'solarRadiance' in df.columns else [],
            'barometricpressure': df['barometricPressure'].tolist() if 'barometricPressure' in df.columns else [],
            'bmealtitude': df['bmealtitude'].tolist() if 'bmealtitude' in df.columns else [],
            'locationLat': df['locationLat'].tolist() if 'locationLat' in df.columns else [],
            'locationLong': df['locationLong'].tolist() if 'locationLong' in df.columns else [],
        }
        
        # Create time labels for charts
        labels = (pd.DataFrame(columns=['NULL'], index=pd.date_range('2022-05-21T00:00:00Z', '2022-05-21T23:00:00Z', freq='30T')).between_time('00:00','23:00').index.strftime('%H:%M').tolist())
        context['labels'] = labels
    
    return context

# New dashboard views
#@login_required(login_url='signin')  # Redirects to signin if not logged in
def user_menu(request):
    
    uname = request.user.username
    
    context = {'fname': uname}
    
    return render(request, 'user_menu.html', context)




@login_required(login_url='signin')  # Redirects to signin if not logged in
def contact(request):
    return render(request, 'contact.html')

# Modified weather_updates view to use the helper function
@login_required(login_url='signin')  # Redirects to signin if not logged in
def weather_updates(request):
    context = get_weather_data()
    return render(request, 'weather_updates.html', context)

# Old dashboard API views
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        context = get_weather_data()
        return render(request, 'weather_updates.html', context=context)

class WeatherUpdate(APIView):
    serializer_class = weatherSerializer
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = weatherSerializer(data=data)
            if serializer.is_valid():
                weatherData.objects.create(
                    relativeHumidity=data.get('humidity'), 
                    airTemperature=data.get('temperature'),
                    windDirection=data.get('windDirection'), 
                    windSpeed=data.get('windSpeed'), 
                    rainfall=data.get('rainfall'), 
                    soilMoisture=data.get('soilmoisture'),
                    soilTemperature=data.get('soiltemperature'), 
                    lightIntensity=data.get('lightintensity'),
                    solarRadiance=data.get('solarradiance'), 
                    barometricPressure=data.get('barometricpressure'),
                    bmealtitude=data.get('bmealtitude'), 
                    locationLat=data.get('locationLat'),
                    locationLong=data.get('locationLong'), 
                    status=data.get('status')
                )
                return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return JsonResponse(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'Exception': str(e)})

@login_required(login_url='signin')  # Redirects to signin if not logged in
def Stations_Interface(request):
    title = 'Stations_Interface'
    station_list = weatherStation.objects.all()
    markers = []

    for station in station_list:
        lat = station.latitude
        lng = station.longitude

        if lat is None or lng is None:
            continue

        markers.append(folium.Marker([lat, lng], tooltip='Click for more',
                     popup=f"{station.station_name}<br>{station.city_name}<br>{station.id}"))

    m = folium.Map(location=[-19.015438, 29.154857], zoom_start=6)

    for marker in markers:
        marker.add_to(m)

    # Get HTML Representation of Map Object
    m_html = m._repr_html_()
    context = {
        'm': m_html,
        'title': title,
    }
    return render(request, 'stations_interface.html', context)