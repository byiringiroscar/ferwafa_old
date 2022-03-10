from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import User_profile
from authentication.forms import ProfileForm, MainProfileForm
from team.forms import TeamForm, Team_Profile_Form, PlayerForm, PlayerProfileForm, RankingTableForm, \
    TableRankingStandingForm, PlayerStatisticsRankingForm, Legend_story_Form, LiveMatchForm, EditScoreForm, \
    CreateTrophyForm, ClubManagerForm
from team.models import Team, Team_profile, Player, Player_profile, Ranking_Table, Table_Ranking, \
    player_statistics_ranking, Legend_story, Live_match, Trophy, Trophy_team, Club_managers
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()


# Create your views here.
@login_required()
def dashboard(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = Team.objects.filter(user=user)
    number_of_team = Team.objects.filter(user=user).count()
    team_first = Team.objects.filter(user=user)
    player_list = []
    for team_f in team_first:
        team_new_player = team_f.player.all().count()
        player_list.append(team_new_player)
    total = 0
    for s in player_list:
        total = total + s
    context = {
        'user': user,
        'profile': user_profile,
        'team': team,
        'number_of_team': number_of_team,
        'total': total,
    }
    return render(request, 'dashboard_home/index.html', context)


@login_required
def team(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = Team.objects.filter(user=user)
    context = {
        'user': user,
        'profile': user_profile,
        'team': team
    }
    return render(request, 'dashboard_home/team.html', context)


@login_required
def player(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = Team.objects.filter(user=user)
    team_player_now = []
    for play in team:
        team_player_now.append(play)
    player_all = []
    for pl in team_player_now:
        new_p = pl.player.all()
        player_all.append(new_p)
    my_objects = Player.objects.none()  # note this return only empty querryset to be added
    qs = my_objects | player_all  # we took all different queryset and merge in one qs
    sum = Team.objects.none()
    for q in qs:
        sum = sum | q  # sum of all player in qs
        print("count all player", sum.count())

    context = {
        'user': user,
        'profile': user_profile,
        'player_all': player_all,
        'team': team,
        'sum': sum
    }
    return render(request, 'dashboard_home/player.html', context)


# add team
@login_required
def add_team(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team_name = form.cleaned_data.get('team_name')
            team_picture = form.cleaned_data.get('team_picture')
            team_president = form.cleaned_data.get('team_president')
            Team.objects.create(team_name=team_name, team_picture=team_picture, team_president=team_president,
                                user=user)
            return redirect('dashboard')
        else:
            form = TeamForm()
    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
    }
    return render(request, 'dashboard_home/add_team.html', context)


# team detail
@login_required
def team_detail(request, id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = get_object_or_404(Team, id=id)
    player = team.player.all().count()
    team_profile = get_object_or_404(Team_profile, team=team)

    context = {
        'team': team,
        'user': user,
        'profile': user_profile,
        'player': player,
        'team_profile': team_profile,
    }
    return render(request, 'dashboard_home/team_detail.html', context)


# complete both profile and main profile
@login_required
def profile(request):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
    if form.is_valid():
        form.save()
        return redirect('profile')

    context = {
        'user': user,
        'profile': user_profile,
        'form': form
    }
    return render(request, 'dashboard_home/profile.html', context)


# main profile
@login_required
def main_profile(request):
    user = request.user
    phone_number = user.phone_number
    user_main = get_object_or_404(User, phone_number=phone_number)
    user_profile = get_object_or_404(User_profile, user=user)
    form = MainProfileForm(request.POST or None, instance=user_main)
    if form.is_valid():
        form.save('main_profile')
    context = {
        'user': user,
        'profile': user_profile,
        'form': form

    }
    return render(request, 'dashboard_home/main_profile.html', context)


# player profile
@login_required
def player_profile(request, id, player_id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = get_object_or_404(Team, id=id)
    player = get_object_or_404(Player, id=player_id)
    player_edit_profile = get_object_or_404(Player_profile, player=player)
    form = PlayerProfileForm()
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST or None, instance=player_edit_profile)
        if form.is_valid():
            form.save()
            return redirect('player_profile', id=team.id, player_id=player.id)

    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'team': team,
        'player': player,
        'player_edit_profile': player_edit_profile,
    }
    return render(request, 'dashboard_home/player_profile.html', context)


# end of completing both profile and main profile
@login_required
def team_profile(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    team = get_object_or_404(Team, id=id)
    profile_team_user = get_object_or_404(Team_profile, team=team)
    form = Team_Profile_Form(request.POST or None, instance=profile_team_user)
    if form.is_valid():
        form.save()
    context = {
        'user': user,
        'profile': user_profile,
        'team': team,
        'team_profile': profile_team_user,
        'form': form
    }
    return render(request, 'dashboard_home/team_profile.html', context)


# edit main team profile
@login_required
def edit_main_team_profile(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    team = get_object_or_404(Team, id=id)
    form = TeamForm(request.POST or None, request.FILES or None, instance=team)
    if form.is_valid():
        form.save()
        return redirect('dashboard')

    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'team': team
    }
    return render(request, 'dashboard_home/edit_main_team_profile.html', context)


# add player
@login_required
def add_player(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    team = get_object_or_404(Team, id=id)
    form = PlayerForm()
    if request.method == 'POST':
        form = PlayerForm(request.POST or None, request.FILES)
        if form.is_valid():
            player_name = form.cleaned_data.get('player_name')
            player_number = form.cleaned_data.get('player_number')
            player_position = form.cleaned_data.get('player_position')
            player_image = form.cleaned_data.get('player_image')
            new_player = Player.objects.create(player_name=player_name, player_number=player_number,
                                               player_position=player_position, player_image=player_image)
            team.player.add(new_player)
            team.save()
            return redirect('add_player', id=id)
    else:
        form = PlayerForm()

    context = {
        'user': user,
        'profile': user_profile,
        'team': team,
        'form': form,
    }
    return render(request, 'dashboard_home/add_player.html', context)


# view player
@login_required
def view_player(request, id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = get_object_or_404(Team, id=id)
    player = team.player.all()
    context = {
        'user': user,
        'profile': user_profile,
        'team': team,
        'player': player,
    }
    return render(request, 'dashboard_home/view_player.html', context)


# view player detail
@login_required
def player_detail(request, id, player_id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    team = get_object_or_404(Team, id=id)
    player = get_object_or_404(team.player, id=player_id)

    context = {
        'user': user,
        'profile': user_profile,
        'player': player,
        'team': team,
    }
    return render(request, 'dashboard_home/player_detail.html', context)


# Create ranking
@login_required
def ranking_table_name(request):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    form = RankingTableForm()
    if request.method == 'POST':
        form = RankingTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ranking')
    else:
        form = RankingTableForm()
    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
    }
    return render(request, 'dashboard_home/ranking_table_name.html', context)


# view all ranking before you rank team
@login_required
def ranking(request):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking = Ranking_Table.objects.all().order_by('-ranking_year')
    context = {
        'user': user,
        'profile': user_profile,
        'ranking': ranking
    }
    return render(request, 'dashboard_home/ranking.html', context)


# choose team to rank
@login_required
def choose_ranking_team(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    team = Team.objects.all()
    ranking_id = get_object_or_404(Ranking_Table, id=id)
    print("ranking ============", ranking_id)
    context = {
        'user': user,
        'profile': user_profile,
        'team': team,
        'ranking_id': ranking_id,
    }
    return render(request, 'dashboard_home/choose_ranking_team.html', context)


@login_required
def ranking_page(request, id, team_id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    form = TableRankingStandingForm()
    ranking_id = get_object_or_404(Ranking_Table, id=id)
    team_id = get_object_or_404(Team, id=team_id)
    team_id_redi = team_id.id
    if request.method == 'POST':
        form = TableRankingStandingForm(request.POST)
        if form.is_valid():
            table_ranking_check = Table_Ranking.objects.filter(team=team_id).filter(ranking=ranking_id)
            if not table_ranking_check.exists():
                instance = form.save(commit=False)
                instance.ranking = ranking_id
                instance.team = team_id
                instance.save()
                return redirect('table_ranking_list')

            elif table_ranking_check.exists():
                messages.error(request, f'{team_id.team_name} Ranking record in season {ranking_id} already stored go '
                                        f'to update it ')
                return redirect('ranking_page', id=id, team_id=team_id_redi)


    else:
        form = TableRankingStandingForm()

    context = {
        'user': user,
        'profile': user_profile,
        'form': form
    }
    return render(request, 'dashboard_home/ranking_page.html', context)


@login_required
def table_ranking_list(request):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking = Ranking_Table.objects.all().order_by('-ranking_year')
    context = {
        'user': user,
        'profile': user_profile,
        'ranking': ranking
    }
    return render(request, 'dashboard_home/table_ranking_list.html', context)


@login_required
def team_table_points(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking_table_season = get_object_or_404(Ranking_Table, id=id)
    table_ranks = Table_Ranking.objects.filter(ranking=ranking_table_season).order_by('-team_points')
    context = {
        'user': user,
        'profile': user_profile,
        'table_ranks': table_ranks,
        'ranking_season': ranking_table_season,
    }
    return render(request, 'dashboard_home/team_table_points.html', context)


@login_required
def edit_table_points(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    table_ranking_points = get_object_or_404(Table_Ranking, id=id)
    table_ranking_id = table_ranking_points.ranking.id
    form = TableRankingStandingForm(request.POST or None, instance=table_ranking_points)
    if request.method == 'POST':
        form = TableRankingStandingForm(request.POST or None, instance=table_ranking_points)
        if form.is_valid():
            form.save()
            return redirect('team_table_points', id=table_ranking_id)

    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'team': table_ranking_points
    }
    return render(request, 'dashboard_home/edit_table_points.html', context)


@login_required
def add_player_stat(request):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking = Ranking_Table.objects.all().order_by('-ranking_year')
    context = {
        'user': user,
        'profile': user_profile,
        'ranking': ranking
    }
    return render(request, 'dashboard_home/add_player_stat.html', context)


@login_required
def rank_player_team(request, id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    rank_season = get_object_or_404(Ranking_Table, id=id)
    team = Team.objects.filter(user=user)
    context = {
        'user': user,
        'profile': user_profile,
        'team': team,
        'rank_season': rank_season
    }
    return render(request, 'dashboard_home/rank_player_team.html', context)


@login_required
def player_rank(request, id, team_id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    rank_id = get_object_or_404(Ranking_Table, id=id).id
    team_player_in = get_object_or_404(Team, id=team_id)
    team_player = team_player_in.player.all()
    context = {
        'user': user,
        'profile': user_profile,
        'player': team_player,
        'rank_id': rank_id,
        'team': team_player_in
    }
    return render(request, 'dashboard_home/player_rank.html', context)


@login_required
def player_rank_points(request, id, team_id, player_id):
    user = request.user
    player_rank_season = get_object_or_404(Ranking_Table, id=id)
    user_profile = User_profile.objects.get(user=user)
    team = get_object_or_404(Team, id=team_id)
    player_id_stat = get_object_or_404(Player, id=player_id)
    form = PlayerStatisticsRankingForm()
    if request.method == 'POST':
        form = PlayerStatisticsRankingForm(request.POST)
        if form.is_valid():
            player_team_check = player_statistics_ranking.objects.filter(player_year_statistics=player_rank_season,
                                                                         player_team=team,
                                                                         player_statistics=player_id_stat)
            if not player_team_check.exists():
                instance = form.save(commit=False)
                instance.player_year_statistics = player_rank_season
                instance.player_statistics = player_id_stat
                instance.player_team = team
                instance.save()
                return redirect('player_rank_official_table')
            elif player_team_check.exists():
                messages.error(request,
                               f'{player_id_stat.player_name} Ranking record in season {player_rank_season} already stored go '
                               f'to update it ')
                return redirect('player_rank_points', id=player_rank_season.id, team_id=team.id,
                                player_id=player_id_stat.id)
    else:
        form = PlayerStatisticsRankingForm()
    context = {
        'user': user,
        'profile': user_profile,
        'form': form
    }
    return render(request, 'dashboard_home/player_rank_points.html', context)


@login_required
def player_rank_official_table(request):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking = Ranking_Table.objects.all().order_by('-ranking_year')
    context = {
        'user': user,
        'profile': user_profile,
        'ranking': ranking
    }
    return render(request, 'dashboard_home/player_rank_official_table.html', context)


@login_required
def player_table_points(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking_table_season = get_object_or_404(Ranking_Table, id=id)
    table_player_ranks = player_statistics_ranking.objects.filter(player_year_statistics=ranking_table_season).order_by(
        '-player_goals')
    context = {
        'user': user,
        'profile': user_profile,
        'table_player_ranks': table_player_ranks,
        'ranking_table_season': ranking_table_season
    }
    return render(request, 'dashboard_home/player_table_points.html', context)


@login_required
def edit_table_player_points(request, id):
    user = request.user
    user_profile = get_object_or_404(User_profile, user=user)
    ranking_player_table = get_object_or_404(player_statistics_ranking, id=id)
    rank_id = ranking_player_table.player_year_statistics.id
    form = PlayerStatisticsRankingForm(request.POST or None, instance=ranking_player_table)
    if request.method == 'POST':
        form = PlayerStatisticsRankingForm(request.POST or None, instance=ranking_player_table)
        if form.is_valid():
            form.save()
            return redirect('player_table_points', id=rank_id)
    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'player': ranking_player_table
    }
    return render(request, 'dashboard_home/edit_table_player_points.html', context)


@login_required
def legend_story(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    legend = Legend_story.objects.all()
    form = Legend_story_Form()
    if request.method == 'POST':
        form = Legend_story_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = Legend_story_Form()
    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'legend': legend
    }
    return render(request, 'dashboard_home/legend_story.html', context)


@login_required
def delete_legend(request, id):
    legend = get_object_or_404(Legend_story, id=id)
    legend.delete()
    return redirect('legend_story')


@login_required
def livematch(request):
    match_football = Live_match.objects.all().order_by('-date')
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    form = LiveMatchForm()
    if request.method == 'POST':
        form = LiveMatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livematch')
    else:
        form = LiveMatchForm()

    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'match': match_football
    }
    return render(request, 'dashboard_home/livematch.html', context)


@login_required
def edit_score(request, id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    live_stat_edit = get_object_or_404(Live_match, id=id)
    form = EditScoreForm(request.POST or None, instance=live_stat_edit)
    if request.method == 'POST':
        form = EditScoreForm(request.POST or None, instance=live_stat_edit)
        if form.is_valid():
            form.save()
            return redirect('livematch')
    context = {
        'user': user,
        'profile': user_profile,
        'form': form
    }

    return render(request, 'dashboard_home/edit_score.html', context)


@login_required
def suspend_match(request, id):
    suspend = Live_match.objects.filter(id=id).update(suspended=True)
    return redirect('livematch')


@login_required
def create_trophy(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    form = CreateTrophyForm()
    if request.method == 'POST':
        form = CreateTrophyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trophy')
    else:
        form = CreateTrophyForm
    context = {
        'user': user,
        'profile': user_profile,
        'form': form
    }
    return render(request, 'dashboard_home/create_trophy.html', context)


@login_required
def trophy(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    all_trophy = Trophy.objects.all()
    context = {
        'user': user,
        'profile': user_profile,
        'trophy': all_trophy
    }
    return render(request, 'dashboard_home/trophy.html', context)


@login_required
def give_team_trophy(request, id):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    all_team = Team.objects.all()
    trophy_name = get_object_or_404(Trophy, id=id)
    context = {
        'user': user,
        'profile': user_profile,
        'team': all_team,
        'trophy': trophy_name,
    }
    return render(request, 'dashboard_home/give_team_trophy.html', context)


@login_required
def confirm_trophy_cup(request, id, team_id):
    trophy_type = get_object_or_404(Trophy, id=id)
    team_trophy = get_object_or_404(Team, id=team_id)
    check_trophy = Trophy_team.objects.filter(trophy=trophy_type, team=team_trophy)
    if check_trophy.exists():
        messages.error("multiple trophy on multiple team not allowed")
        context = {'messages': messages}
        return redirect('give_team_trophy', id=trophy_type.id)
    if not check_trophy.exists():
        trophy_team = Trophy_team.objects.create(trophy=trophy_type, team=team_trophy)
        return redirect('dashboard')


@login_required
def add_manager(request):
    user = request.user
    user_profile = User_profile.objects.get(user=user)
    all_coaches = Club_managers.objects.all()
    form = ClubManagerForm()
    if request.method == 'POST':
        form = ClubManagerForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_manager')
    else:
        form = ClubManagerForm()

    context = {
        'user': user,
        'profile': user_profile,
        'form': form,
        'manager': all_coaches
    }
    return render(request, 'dashboard_home/add_manager.html', context)
