from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from authentication.forms import UserRegistrationForm
from team.models import Team, Team_profile, Player, Player_profile, Trophy_team, Table_Ranking, Live_match, \
    Ranking_Table, player_statistics_ranking, Legend_story, Connect_message
from datetime import datetime
from team.forms import ConnectMessageForm
from team.models import Club_managers
from .utilis import Util
import itertools
import functools
from django.contrib import messages
from django.db.models import Q

now_time = datetime.now()


# Create your views here.
def create_account(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'home_view/create_account.html', context)


def home(request):
    live_match = Live_match.objects.filter(suspended=False).order_by('-id')
    live_match_first = Live_match.objects.all().order_by('-id').first()
    latest_ranking_table = Ranking_Table.objects.all().order_by('-ranking_year')[0]
    player_goals_stat = player_statistics_ranking.objects.filter(player_year_statistics=latest_ranking_table).order_by(
        '-player_goals')[:11]
    player_assist_stat = player_statistics_ranking.objects.filter(player_year_statistics=latest_ranking_table).order_by(
        '-player_assist')[:11]
    player_goalkeeper_stat = player_statistics_ranking.objects.filter(
        player_year_statistics=latest_ranking_table).order_by(
        '-player_clean_shit')[:11]
    player_goals_stat_slide = player_statistics_ranking.objects.filter(
        player_year_statistics=latest_ranking_table).order_by(
        '-player_goals').first()
    player_assist_slide = player_statistics_ranking.objects.filter(
        player_year_statistics=latest_ranking_table).order_by(
        '-player_assist').first()
    player_clean_sheet_slide = player_statistics_ranking.objects.filter(
        player_year_statistics=latest_ranking_table).order_by(
        '-player_clean_shit').first()
    match_done_in_past = Live_match.objects.filter(date__gte=now_time)

    coach = Club_managers.objects.all()
    legend_story = Legend_story.objects.all().first()
    context = {
        'live_match': live_match,
        'live_match_first': live_match_first,
        'player_goals': player_goals_stat,
        'player_assist': player_assist_stat,
        'player_clean_sheet': player_goalkeeper_stat,
        'player_goals_slide': player_goals_stat_slide,
        'player_assist_slide': player_assist_slide,
        'player_clean_sheet_slide': player_clean_sheet_slide,
        'legend_story': legend_story,
        'coach': coach,
        'match_done': match_done_in_past
    }
    return render(request, 'home_view/index.html', context)


def standings(request):
    standing_year = Ranking_Table.objects.all().order_by('-ranking_year')
    ranking_table_year = Table_Ranking.objects.all()
    counter = functools.partial(next, itertools.count(1))

    context = {
        'standing': standing_year,
        'ranking_table_year': ranking_table_year,
        'counter': counter
    }
    return render(request, 'home_view/standings.html', context)


def matchlive(request):
    match_li = Live_match.objects.filter(date__gte=now_time)
    context = {
        'match_live': match_li,
        'now_time': now_time
    }
    return render(request, 'home_view/matchlive.html', context)


def upcoming(request):
    upcoming_m = Live_match.objects.filter(date__gt=now_time)
    context = {
        'upcoming_match': upcoming_m
    }
    return render(request, 'home_view/upcoming.html', context)


def search(request):
    return render(request, 'home_view/search.html')


def contact(request):
    return render(request, 'home_view/contact.html')


def club_team(request):
    team = Team.objects.filter(visibility=True)
    context = {
        'team': team
    }
    return render(request, 'home_view/club_team.html', context)


def home_team_detail(request, id):
    now_time_slide = datetime.today().date()
    team_detail = get_object_or_404(Team, id=id)
    team_prof = get_object_or_404(Team_profile, team=team_detail)
    ranking_table_year_first = Ranking_Table.objects.all().order_by('-ranking_year')[0]
    table_ranking = Table_Ranking.objects.filter(ranking=ranking_table_year_first)
    table_check_win_loss = Table_Ranking.objects.filter(team=team_detail, ranking=ranking_table_year_first).exists()
    counter = functools.partial(next, itertools.count(1))
    if table_check_win_loss:
        table_win_loss = get_object_or_404(Table_Ranking, team=team_detail, ranking=ranking_table_year_first)
        win = table_win_loss.win
        loss = table_win_loss.loss
        game_played = table_win_loss.game_played
        win_percent = (win * 100) / game_played
        loss_percent = (loss * 100) / game_played
    elif not table_check_win_loss:
        win_percent = 1
        loss_percent = 1

    context = {
        'team': team_detail,
        'team_prof': team_prof,
        'table_ranking': table_ranking,
        'win_percent': win_percent,
        'loss_percent': loss_percent,
        'now_time': now_time_slide,
        'counter': counter
    }
    return render(request, 'home_view/home_team_detail.html', context)


def home_team_player(request, id):
    team_detail = get_object_or_404(Team, id=id)
    player_team = team_detail.player.all()
    context = {
        'player': player_team,
        'team': team_detail
    }
    return render(request, 'home_view/home_team_player.html', context)


def home_player_detail(request, id, player_id):
    team = get_object_or_404(Team, id=id)
    player = get_object_or_404(Player, id=player_id)
    player_profile = get_object_or_404(Player_profile, player=player)
    player_trophy = Trophy_team.objects.filter(team=team)
    player_trophy_ex = Trophy_team.objects.filter(team=team)
    all_player_stat = player_statistics_ranking.objects.filter(player_statistics=player).order_by(
        '-player_year_statistics__ranking_year')

    context = {
        'team': team,
        'player': player,
        'player_profile': player_profile,
        'player_trophy': player_trophy,
        'player_trophy_ex': player_trophy_ex,
        'all_player_stat': all_player_stat,

    }
    return render(request, 'home_view/home_player_detail.html', context)


def home_upcoming_match(request):
    upcoming_match = Live_match.objects.all().filter(date__gte=now_time, suspended=False)
    upcoming_match_first = Live_match.objects.all().filter(date__gte=now_time, suspended=False).first()
    context = {
        'upcoming_match': upcoming_match,
        'upcoming_match_first': upcoming_match_first
    }
    return render(request, 'home_view/home_upcoming_match.html', context)


def home_manager_detail(request, id):
    manager_detail = get_object_or_404(Club_managers, id=id)
    manager_team = manager_detail.current_team
    manager_rank_year = manager_detail.current_season
    manager_formation = str(manager_detail.managers_formation)
    manager_trophy = manager_detail.manager_trophy.all()
    manager_table_rank = Table_Ranking.objects.filter(team=manager_team).filter(ranking=manager_rank_year)
    win = 0
    loss = 0
    game_played = 0
    for manager_rate in manager_table_rank:
        manager_win = win + manager_rate.win
        manager_loss = loss + manager_rate.loss
        manager_game = game_played + manager_rate.game_played
    win_percentage = (manager_win * 100) / manager_game
    loss_percentage = (manager_loss * 100) / manager_game



    context = {
        'coach': manager_detail,
        'manager_formation': manager_formation,
        'manager_trophy': manager_trophy,
        'manager_table_rank': manager_table_rank,
        'win_percentage': int(win_percentage),
        'loss_percentage': int(loss_percentage)
    }
    return render(request, 'home_view/home_manager_detail.html', context)


def home_contact_connect(request, id, player_id):
    team_contact = get_object_or_404(Team, id=id)
    player_contact = get_object_or_404(Player, id=player_id)
    team_contact_email = team_contact.team_email_transfer
    form = ConnectMessageForm()

    if request.method == 'POST':
        form = ConnectMessageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            subject = form.cleaned_data.get('subject')
            email = form.cleaned_data.get('email')
            body = form.cleaned_data.get('body')
            scout_file = form.cleaned_data.get('file_field')
            body_message = f' \n {body} \n my contact is : \n {email} '
            Connect_message.objects.create(team=team_contact, player=player_contact, name=name, subject=subject,
                                           email=email, connect_file=scout_file, body=body_message)
            data = {'email_subject': subject, 'email_body': body_message, 'to_email': team_contact_email}
            Util.send_email(data, scout_file)
            messages.info(request, "Your message sent successful")
            return redirect('home_contact_connect', id=team_contact.id, player_id=player_contact.id)
    else:
        form = ConnectMessageForm()

    context = {
        'team': team_contact,
        'player': player_contact,
        'form': form
    }
    return render(request, 'home_view/home_contact_connect.html', context)
