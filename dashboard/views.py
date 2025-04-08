from django.shortcuts import render

def admin_menu(request):
    return render(request, 'admin-menu.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def index2(request):
    return render(request, 'index2.html')

def live_cameras(request):
    return render(request, 'live-cameras.html')

def main_menu(request):
    return render(request, 'main-menu.html')

def news(request):
    return render(request, 'news.html')

def single(request):
    return render(request, 'single.html')

