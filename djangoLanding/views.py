from django.shortcuts import redirect, render
from userLogs.views import signin, signup

# Create your views here.
def index(request):
    return render(request, 'djangoLanding/index.html')
