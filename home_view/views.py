from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    return render(request, 'home_view/index.html')


def standings(request):
    return render(request, 'home_view/standings.html')


def matchlive(request):
    return render(request, 'home_view/matchlive.html')


def upcoming(request):
    return render(request, 'home_view/upcoming.html')


def search(request):
    return render(request, 'home_view/search.html')


def contact(request):
    return render(request, 'home_view/contact.html')



