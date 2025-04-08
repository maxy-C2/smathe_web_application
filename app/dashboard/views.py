from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.views.generic import View
import pandas as pd
import json

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import weatherdata
from .serializers import weatherSerializer

from django.shortcuts import render
from django.db.models import Q
from .models import Station
import folium
import geocoder


def Stations_interface(request):
    title = 'Stations_Interface'
    search_query = request.GET.get('city')  # Get the search query from the URL parameters
    Wstations = Place.objects.all()
    markers = []

    if search_query:
        # Filter Wstations based on the search query (city)
        Wstations = Wstations.filter(Q(city__icontains=search_query))

    for Wstation in Wstations:
        latitude = Wstation.latitude
        longitude = Wstation.longitude

        if latitude is not None and longitude is not None:
            # Create a Folium Marker for the Wstation
            marker = folium.Marker([latitude, longitude], popup=Wstation.name)
            markers.append(marker)

    # Create a Folium map centered at a specific location
    map_center = [latitude, longitude]  # Specify the center coordinates
    my_map = folium.Map(location=map_center, zoom_start=10)

    # Add the markers to the map
    for marker in markers:
        marker.add_to(my_map)

    # Render the map and return it as a response
    map_html = my_map._repr_html_()
    return render(request, 'stations_inteface.html', {'stations_inteface_html': map_html})
    """
    station_list = Station.objects.all()
    markers = []

    for Wstation in station_list:
        lat = Wstation.latitude
        lng = Wstation.longitude
        country = location.country

        if lat == None or lng == None:
            continue

        markers.append(folium.Marker([lat, lng], tooltip='Click for more',
                      popup=f"{Wstation.Wstation}<br>{country}"))

    m = folium.Map(location=[-19.015438, 29.154857], zoom_start=6)

    for marker in markers:
        marker.add_to(m)

    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'title': title,
    }
    return render(request, 'stations_interface.html', context)
    """
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        
        item = weatherdata.objects.all().values()
        df = pd.DataFrame(item)
        humidity = df['humidity'].tolist()
        temperature = df['temperature'].tolist()
        windDirection = df['windDirection'].tolist()
        windSpeed = df['windSpeed'].tolist()
        rainfall = df['rainfall'].tolist()
        soilmoisture = df['soilmoisture'].tolist()
        soiltemperature = df['soiltemperature'].tolist()
        lightintensity = df['lightintensity'].tolist()
        solarradiance = df['solarradiance'].tolist()
        barometricpressure = df['barometricpressure'].tolist()
        bmealtitude = df['bmealtitude'].tolist()
        locationLat = df.locationLat.tolist()
        locationLong = df.locationLong.tolist()
        #status = df['status'].tolist()
        
        labels = (pd.DataFrame(columns=['NULL'], index=pd.date_range('2022-05-21T00:00:00Z', '2022-05-21T23:00:00Z', freq='30T')).between_time('00:00','23:00').index.strftime('%H:%M').tolist())
        
        mydict = {
            'humidity': humidity,
            'temperature':temperature,
            'windDirection':windDirection,
            'windSpeed':windSpeed,
            'rainfall':rainfall,
            'soilmoisture':soilmoisture,
            'soiltemperature':soiltemperature,
            'lightintensity':lightintensity,
            'solarradiance':solarradiance,
            'barometricpressure':barometricpressure,
            'bmealtitude':bmealtitude,
            'locationLat':locationLat,
            'locationLong':locationLong,
            #'status':status,
            'labels':labels
        }
        
        return render(request, 'dashboard/home.html', context=mydict) 
    
class WeatherUpdate(APIView):
    
    """
        WEATHER UPDATE VIEW
    """
    
    serializer_class = weatherSerializer
    
    # def get(self, request, format=None):
        
    #     try :
    #         data = json.loads(request.body)
    #         serializer = weatherSerializer(data=data)
    #         if serializer.is_valid():
    #             weatherdata.objects.create(
    #                     humidity=data.post('humidity'), temperature=data.post('temperature'),
    #                     windDirection=data.post('windDirection'), windSpeed=data.post('windSpeed'), 
    #                     rainfall=data.post('rainfall'), soilmoisture=data.post('soilmoisture'),
    #                     soiltemperature=data.post('soiltemperature'), lightintensity=data.post('lightintensity'),
    #                     solarradiance=data.post('solarradiance'), barometricpressure=data.post('barometricpressure'),
    #                     bmealtitude=data.post('bmealtitude'), locationLat=data.post('locationLat'),
    #                     locationLong=data.post('locationLong'), status=data.post('status')
    #              )
    #             return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
    #         else:
    #             return JsonResponse(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)
    #     except Exception as e:
    #         return JsonResponse(status=status.HTTP_404_NOT_FOUND, data={'Exception' : e})

    def post(self, request):
        try :
            data = json.loads(request.body)
            serializer = weatherSerializer(data=data)
            if serializer.is_valid():
                weatherdata.objects.create(
                        humidity=data.get('humidity'), temperature=data.get('temperature'),
                        windDirection=data.get('windDirection'), windSpeed=data.get('windSpeed'), 
                        rainfall=data.get('rainfall'), soilmoisture=data.get('soilmoisture'),
                        soiltemperature=data.get('soiltemperature'), lightintensity=data.get('lightintensity'),
                        solarradiance=data.get('solarradiance'), barometricpressure=data.get('barometricpressure'),
                        bmealtitude=data.get('bmealtitude'), locationLat=data.get('locationLat'),
                        locationLong=data.get('locationLong'), status=data.get('status')
                 )
                return JsonResponse(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return JsonResponse(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'Exception' : e})
    