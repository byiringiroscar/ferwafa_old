from django.urls import path
from .views import dashboard, add_team, profile, team_detail, main_profile, team_profile, add_player, view_player, \
    player_detail, player_profile, team, player, ranking_table_name, ranking, choose_ranking_team, ranking_page, table_ranking_list, team_table_points, edit_table_points, add_player_stat, \
rank_player_team, player_rank, player_rank_points, player_rank_official_table, player_table_points, edit_table_player_points, edit_main_team_profile, legend_story, delete_legend, livematch, edit_score, suspend_match, create_trophy, trophy, give_team_trophy, confirm_trophy_cup, add_manager, dashboard_contact_inbox

name = 'team'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    # team
    path('team', team, name='team'),
    # player
    path('player/', player, name='player'),
    # add team
    path('add_team/', add_team, name='add_team'),
    # team detail
    path('team_detail/<int:id>/', team_detail, name='team_detail'),
    # team profile complete
    path('team_detail/<int:id>/team_profile', team_profile, name='team_profile'),
    # edit main team profile
    path('team_detail/<int:id>/team_profile/edit_main_team_profile/', edit_main_team_profile, name='edit_main_team_profile'),
    # end of team profile
    # player profile
    path('team_detail/<int:id>/view_player/<player_id>/player_profile/', player_profile, name='player_profile'),
    # add player to the team
    path('team_detail/<int:id>/add_player/', add_player, name='add_player'),
    # view team player
    path('team_detail/<int:id>/view_player/', view_player, name='view_player'),
    # end of adding the team
    # view player detail
    path('team_detail/<int:id>/view_player/<player_id>/', player_detail, name='player_detail'),
    path('profile/', profile, name='profile'),
    path('main_profile/', main_profile, name='main_profile'),
    # path for create ranking name
    path('ranking_table_name/', ranking_table_name, name='ranking_table_name'),
    # ranking name
    path('ranking/', ranking, name='ranking'),
    # choose team to rank in choose_ranking_team
    path('ranking/<int:id>/choose_ranking_team/', choose_ranking_team, name='choose_ranking_team'),
    # page of form to rank first team
    path('ranking/<int:id>/choose_ranking_team/<team_id>/', ranking_page, name='ranking_page'),
    # choose season ranking in each item ranking
    path('table_ranking_list/', table_ranking_list, name='table_ranking_list'),
    # team table list with points and season as well
    path('table_ranking_list/<int:id>/team_table_points/', team_table_points, name='team_table_points'),
    # edit table team points single
    path('table_ranking_list/<int:id>/team_table_points/edit_table_points/', edit_table_points, name='edit_table_points'),
    # add player statistics with start with choose ranking
    path('add_player_stat/', add_player_stat, name='add_player_stat'),
    # choose player to team to rank
    path('add_player_stat/<int:id>/rank_player_team/', rank_player_team, name='rank_player_team'),
    # player of certain team to rank
    path('add_player_stat/<int:id>/rank_player_team/<team_id>/player_rank/', player_rank, name='player_rank'),
    # give player initial points
    path('add_player_stat/<int:id>/rank_player_team/<team_id>/player_rank/<player_id>', player_rank_points, name='player_rank_points'),
    # player ranking official choose season
    path('player_rank_official_table/', player_rank_official_table, name='player_rank_official_table'),
    # player table and edit option
    path('player_rank_official_table/<int:id>/player_table_points/', player_table_points, name='player_table_points'),
    # edit player table points
    path('player_rank_official_table/<int:id>/player_table_points/edit_table_player_points/', edit_table_player_points, name='edit_table_player_points'),
    # add legend story
    path('legend_story/', legend_story, name='legend_story'),
    # delete legend
    path('delete_legend/<int:id>/', delete_legend, name='delete_legend'),
    # Live match path
    path('livematch/', livematch, name='livematch'),
    # edit live score
    path('livematch/<int:id>/edit_score/', edit_score, name='edit_score'),
    # suspend match
    path('livematch/<int:id>/suspend_match/', suspend_match, name='suspend_match'),
    # create trophy
    path('create_trophy/', create_trophy, name='create_trophy'),
    # view trophy and give to team
    path('trophy/', trophy, name='trophy'),
    # choose  team trophy
    path('trophy/<int:id>/give_team_trophy/', give_team_trophy, name='give_team_trophy'),
    # confirm team trophy
    path('trophy/<int:id>/give_team_trophy/<team_id>/', confirm_trophy_cup, name='confirm_trophy_cup'),
    # add club manager and view
    path('add_manager/', add_manager, name='add_manager'),
    # path for all inbox message
    path('dashboard_contact_inbox/', dashboard_contact_inbox, name='dashboard_contact_inbox')

]
