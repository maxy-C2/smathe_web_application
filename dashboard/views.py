from django.shortcuts import render


def user_menu(request):
    return render(request, 'user_menu.html')

def weather_updates(request):
    return render(request, 'weather_updates.html')

def contact(request):
    return render(request, 'contact.html')
