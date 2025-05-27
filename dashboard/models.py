from django.db import models


# Keep the old dashboard's weatherData model
class weatherStation(models.Model):
    city_name = models.CharField(max_length=100)
    station_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.station_name

class weatherData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    airTemperature = models.CharField(max_length=100, null=True)
    solarRadiance = models.CharField(max_length=100, null=True)
    barometricPressure = models.CharField(max_length=100, null=True)
    lightIntensity = models.CharField(max_length=100, null=True)
    rainfall = models.CharField(max_length=100, null=True)
    relativeHumidity = models.CharField(max_length=100, null=True)
    soilMoisture = models.CharField(max_length=100, null=True)
    soilTemperature = models.CharField(max_length=100, null=True)
    windDirection = models.CharField(max_length=100, null=True)
    windSpeed = models.CharField(max_length=100, null=True)
    bmealtitude = models.CharField(max_length=100, null=True)
    locationLat = models.CharField(max_length=100, null=True)
    locationLong = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True)
    
    def __str__(self):
        return str(self.created)
    
    class Meta:
        ordering = ['created']
        verbose_name_plural = 'weatherData'
    
    @classmethod
    def save_data(cls, data: dict):
        cls.objects.create(
            relativeHumidity=data.get('relativeHumidity'), 
            airTemperature=data.get('airTemperature'),
            windDirection=data.get('windDirection'), 
            windSpeed=data.get('windSpeed'), 
            rainfall=data.get('rainfall'), 
            soilMoisture=data.get('soilMoisture'),
            soilTemperature=data.get('soilTemperature'), 
            lightIntensity=data.get('lightIntensity'),
            solarRadiance=data.get('solarRadiance'), 
            barometricPressure=data.get('barometricPressure'),
            bmealtitude=data.get('bmealtitude'), 
            locationLat=data.get('locationLat'),
            locationLong=data.get('locationLong'), 
            status=data.get('status'),
        )

# Also add Search model that was referenced in forms.py
class search(models.Model):
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.address