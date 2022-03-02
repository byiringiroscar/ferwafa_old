from django.urls import path
from .views import home, standings, matchlive, upcoming, search, contact
from django.contrib.auth import views as authViews

name = 'home_view'
urlpatterns = [
    path('', home, name='home_view'),
    path('standings/', standings, name='standings'),
    path('matchlive/', matchlive, name='matchlive'),
    path('upcoming/', upcoming, name='upcoming'),
    path('search/', search, name='search'),
    path('contact/', contact, name='contact'),
    path('login/', authViews.LoginView.as_view(template_name='home_view/login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'home_view'}, name='logout'),
]
