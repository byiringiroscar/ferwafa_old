from django.urls import path
from .views import home, standings, matchlive, upcoming, search, contact, create_account, club_team, home_team_detail, home_team_player, home_player_detail,home_upcoming_match, home_manager_detail, home_contact_connect
from django.contrib.auth import views as authViews
from django.contrib.auth import views as auth_views

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
    # path for connect with player
    path('club_team/<int:id>/home_team_player/<player_id>/home_contact_connect/', home_contact_connect, name='home_contact_connect'),
    # upcoming match
    path('home_upcoming_match/', home_upcoming_match, name='home_upcoming_match'),
    # manager section detail
    path('manager/<int:id>/', home_manager_detail, name='home_manager_detail'),
    # reset password
    # if error come s you need to allow less secure app secure go then allow  https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbUZTNUc5VkNFS0dTTUlJa2dYU0l3dEtuM0dzUXxBQ3Jtc0tsNUZMbHJaVTZrZlpsalFvdVBvLUVJYVhyZWRxMDZPR0lFQnRLLXRPOE55S1YydEdMWEp2NUpQdlV3X2xObER2UW04WGhIZDZyMDM0c2xETVhmd21KVHRvUEpCOXJVc21JQkZ6NDMyY005X2tYV1Bybw&q=https%3A%2F%2Fmyaccount.google.com%2Flesssecureapps&v=sFPcd6myZrY
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='home_view/password_reset.html'), name='reset_password'), # here also we are going to customise our own template

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='home_view/password_reset_sent.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home_view/password_reset_form.html'), name='password_reset_confirm'),


    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home_view/password_reset_done.html'), name='password_reset_complete'),
    # then we go in settings.py for configure email password sent
]
