from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from authentication.forms import UserRegistrationForm
from team.models import Team, Team_profile, Player, Player_profile, Trophy_team, Table_Ranking, Live_match


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
    live_match = Live_match.objects.all().order_by('-id')
    context = {
        'live_match': live_match
    }
    return render(request, 'home_view/index.html', context)


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


def club_team(request):
    team = Team.objects.all()
    context = {
        'team': team
    }
    return render(request, 'home_view/club_team.html', context)


def home_team_detail(request, id):
    team_detail = get_object_or_404(Team, id=id)
    team_prof = get_object_or_404(Team_profile, team=team_detail)
    table_ranking = Table_Ranking.objects.filter(team=team_detail).order_by('-ranking')
    print("table-----------------", table_ranking)
    context = {
        'team': team_detail,
        'team_prof': team_prof,
        'table_ranking': table_ranking
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

    context = {
        'team': team,
        'player': player,
        'player_profile': player_profile,
        'player_trophy': player_trophy,
        'player_trophy_ex': player_trophy_ex
    }
    return render(request, 'home_view/home_player_detail.html', context)
