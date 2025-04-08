from django.db import models
#new
class Station(models.Model):
    #country_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    station_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.station_name
    
#new

class weatherdata(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    airTemperature = models.CharField(max_length=100, null=True)
    solarRadiance = models.CharField(max_length=100,  null=True)
    barometricPressure = models.CharField(max_length=100,  null=True)
    lightIntensity = models.CharField(max_length=100, null=True)
    rainfall = models.CharField(max_length=100, null=True)
    relativeHumidity = models.CharField(max_length=100, null=True)
    soilMoisture = models.CharField(max_length=100, null=True)
    soilTemperature = models.CharField(max_length=100, null=True)
    windDirection = models.CharField(max_length=100, null=True)
    windSpeed = models.CharField(max_length=100, null=True)
    bmealtitude = models.CharField(max_length=100, null=True)
    locationLat = models.CharField(max_length=100, null=True)
    locationLong = models.CharField(max_length=100,  null=True)
    status = models.BooleanField(max_length=100,  null=True)  
    
    def __str__(self):
        return str(self.created)
       
    class Meta:
        ordering = ['created']
        
    class Meta:
           verbose_name_plural = 'weatherdata'
    
    def save_data(cls, data : dict):
        cls.create(
            relativeHumidity=data.get('relativeHumidity'), airTemperature=data.get('airTemperature'),
            windDirection=data.get('windDirection'), windSpeed=data.get('windSpeed'), 
            rainfall=data.get('rainfall'), soilMoisture=data.get('soilMoisture'),
            soilTemperature=data.get('soilTemperature'), lightIntensity=data.get('lightIntensity'),
            solarRadiance=data.get('solarRadiance'), barometricPressure=data.get('barometricPressure'),
            bmealtitude=data.get('bmealtitude'), locationLat=data.get('locationLat'),
            locationLong=data.get('locationLong'), status=data.get('status'),
        )