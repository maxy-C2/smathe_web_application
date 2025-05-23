# Generated by Django 3.2.12 on 2022-05-18 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='weatherdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humidity', models.CharField(max_length=100, null=True)),
                ('temperature', models.CharField(max_length=100, null=True)),
                ('windDirection', models.CharField(max_length=100, null=True)),
                ('windSpeed', models.CharField(max_length=100, null=True)),
                ('rainfall', models.CharField(max_length=100, null=True)),
                ('soilmoisture', models.CharField(max_length=100, null=True)),
                ('soiltemperature', models.CharField(max_length=100, null=True)),
                ('lightintensity', models.CharField(max_length=100, null=True)),
                ('solarradiance', models.CharField(max_length=100, null=True)),
                ('barometricpressure', models.CharField(max_length=100, null=True)),
                ('bmealtitude', models.CharField(max_length=100, null=True)),
                ('locationLat', models.CharField(max_length=100, null=True)),
                ('locationLong', models.CharField(max_length=100, null=True)),
                ('status', models.BooleanField(max_length=100, null=True)),
            ],
        ),
    ]
