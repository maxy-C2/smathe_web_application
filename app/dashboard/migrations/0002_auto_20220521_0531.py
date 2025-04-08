# Generated by Django 3.2.13 on 2022-05-21 03:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weatherdata',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
