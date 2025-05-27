from rest_framework import serializers
from .models import weatherData

class weatherSerializer(serializers.Serializer):
    humidity = serializers.CharField(max_length=100, required=True)
    temperature = serializers.CharField(max_length=100, required=True)
    windDirection = serializers.CharField(max_length=100, required=True)
    windSpeed = serializers.CharField(max_length=100, required=True)
    rainfall = serializers.CharField(max_length=100, required=True)
    soilmoisture = serializers.CharField(max_length=100, required=True)
    soiltemperature = serializers.CharField(max_length=100, required=True)
    lightintensity = serializers.CharField(max_length=100, required=True)
    solarradiance = serializers.CharField(max_length=100, required=True)
    barometricpressure = serializers.CharField(max_length=100, required=True)
    bmealtitude = serializers.CharField(max_length=100, required=True)
    locationLat = serializers.CharField(max_length=100, required=True)
    locationLong = serializers.CharField(max_length=100, required=True)
    status = serializers.BooleanField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `weatherdata` instance, given the validated data.
        """
        return weatherData.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `weatherdata` instance, given the validated data.
        """
        instance.relativeHumidity = validated_data.get('humidity', instance.relativeHumidity)
        instance.airTemperature = validated_data.get('temperature', instance.airTemperature)
        instance.windDirection = validated_data.get('windDirection', instance.windDirection)
        instance.windSpeed = validated_data.get('windSpeed', instance.windSpeed)
        instance.rainfall = validated_data.get('rainfall', instance.rainfall)
        instance.soilMoisture = validated_data.get('soilmoisture', instance.soilMoisture)
        instance.soilTemperature = validated_data.get('soiltemperature', instance.soilTemperature)
        instance.lightIntensity = validated_data.get('lightintensity', instance.lightIntensity)
        instance.solarRadiance = validated_data.get('solarradiance', instance.solarRadiance)
        instance.barometricPressure = validated_data.get('barometricpressure', instance.barometricPressure)
        instance.bmealtitude = validated_data.get('bmealtitude', instance.bmealtitude)
        instance.locationLat = validated_data.get('locationLat', instance.locationLat)
        instance.locationLong = validated_data.get('locationLong', instance.locationLong)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance