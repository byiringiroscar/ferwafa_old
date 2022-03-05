from django.urls import path
from .views import home, standings, matchlive, upcoming, search, contact, create_account, club_team, home_team_detail, home_team_player, home_player_detail,home_upcoming_match
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
    path('create_account/', create_account, name='create_account'),
    # path for club team
    path('club_team/', club_team, name='club_team'),
    # home team detail
    path('club_team/<int:id>/home_team_detail/', home_team_detail, name='home_team_detail'),
    # team player
    path('club_team/<int:id>/home_team_player/', home_team_player, name='home_team_player'),
    # path for player detail
    path('club_team/<int:id>/home_team_player/<player_id>', home_player_detail, name='home_player_detail'),
    # upcoming match
    path('home_upcoming_match/', home_upcoming_match, name='home_upcoming_match')
]
