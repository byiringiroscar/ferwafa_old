from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from authentication.forms import UserRegistrationForm
from team.models import Team, Team_profile, Player, Player_profile, Trophy_team, Table_Ranking, Live_match, \
    Ranking_Table, player_statistics_ranking, Legend_story, Connect_message
from datetime import datetime
from team.forms import ConnectMessageForm
from team.models import Club_managers
from .utilis import Util

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
    context = {
        'standing': standing_year,
        'ranking_table_year': ranking_table_year
    }
    return render(request, 'home_view/standings.html', context)


def matchlive(request):
    return render(request, 'home_view/matchlive.html')


def upcoming(request):
    return render(request, 'home_view/upcoming.html')


def search(request):
    return render(request, 'home_view/search.html')


def contact(request):
    return render(request, 'home_view/contact.html')


def club_team(request):
    team = Team.objects.all()
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
        'now_time': now_time_slide
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
    upcoming_match = Live_match.objects.all().filter(date__gte=now_time)
    upcoming_match_first = Live_match.objects.all().filter(date__gte=now_time).first()
    context = {
        'upcoming_match': upcoming_match,
        'upcoming_match_first': upcoming_match_first
    }
    return render(request, 'home_view/home_upcoming_match.html', context)


def home_manager_detail(request, id):
    manager_detail = get_object_or_404(Club_managers, id=id)
    manager_formation = str(manager_detail.managers_formation)

    context = {
        'coach': manager_detail,
        'manager_formation': manager_formation,
    }
    return render(request, 'home_view/home_manager_detail.html', context)


def home_contact_connect(request, id, player_id):
    team_contact = get_object_or_404(Team, id=id)
    player_contact = get_object_or_404(Player, id=player_id)
    form = ConnectMessageForm()
    if request.method == 'POST':
        form = ConnectMessageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            subject = form.cleaned_data.get('subject')
            email = form.cleaned_data.get('email')
            body = form.cleaned_data.get('body')
            Connect_message.objects.create(team=team_contact, player=player_contact, name=name, subject=subject, email=email, body=body)
            data = {'email_subject': subject, 'email_body': body, 'to_email': 'byiringoroscar@gmail.com'}
            Util.send_email(data)
            return redirect('home_view')
    else:
        form = ConnectMessageForm()

    context = {
        'team': team_contact,
        'player': player_contact,
        'form': form
    }
    return render(request, 'home_view/home_contact_connect.html', context)

