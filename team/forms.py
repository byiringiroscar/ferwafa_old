from django import forms
from team.models import Team, Team_profile, Player, Player_profile, Ranking_Table, Table_Ranking, \
    player_statistics_ranking, Legend_story, Live_match, Trophy, Trophy_team
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

now = timezone.now()
from ckeditor.widgets import CKEditorWidget


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_picture', 'team_president']


class Team_Profile_Form(forms.ModelForm):
    team_founded = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    team_contact = forms.EmailField(max_length=200, required=False)

    class Meta:
        model = Team_profile
        fields = ['team_stadium', 'team_location', 'team_founded', 'team_contact', 'team_link']


class PlayerForm(forms.ModelForm):
    player_image = forms.ImageField()

    class Meta:
        model = Player
        fields = ['player_name', 'player_number', 'player_position', 'player_image']


class PlayerProfileForm(forms.ModelForm):
    player_link = forms.URLField(label='Your website', required=False)
    player_height = forms.CharField(label='Your height in meter and centimeter', required=False)
    player_contact = forms.EmailField(label='your email', required=False)
    player_born = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        label='Date of birth',
        required=False
    )

    class Meta:
        model = Player_profile
        fields = ['player_height', 'player_born', 'player_contact', 'player_link']

    def clean_player_born(self):
        player_born = self.cleaned_data['player_born']
        check_time = isinstance(player_born, datetime.date)
        if not check_time:
            raise ValidationError("invalid date check again")
        elif player_born.year > now.year:
            raise ValidationError("Born age must not be greater now date")
        return player_born


class RankingTableForm(forms.ModelForm):
    ranking_year = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        label='Table Year',
        required=True
    )
    ranking_name = forms.CharField(label='League Name', required=False)

    class Meta:
        model = Ranking_Table
        fields = ['ranking_year', 'ranking_name']


class TableRankingStandingForm(forms.ModelForm):
    win = forms.IntegerField(label='Game team won', required=True)
    draw = forms.IntegerField(label='Game team draw', required=True)
    loss = forms.IntegerField(label='Game team lost', required=True)

    class Meta:
        model = Table_Ranking
        fields = ['win', 'draw', 'loss']

    def clean_win(self):
        win = self.cleaned_data['win']
        if win < 0:
            raise ValidationError("win match must be equal to 0 or greater 0")

        return win

    def clean_draw(self):
        draw = self.cleaned_data['draw']
        if draw < 0:
            raise ValidationError("draw match must be equal to 0 or greater 0")
        return draw

    def clean_loss(self):
        loss = self.cleaned_data['loss']
        if loss < 0:
            raise ValidationError("lost match must be equal to 0 or greater 0")
        return loss


class PlayerStatisticsRankingForm(forms.ModelForm):
    player_goals = forms.IntegerField(label='Player Goal', required=True)
    player_assist = forms.IntegerField(label='Player Assist', required=True)

    class Meta:
        model = player_statistics_ranking
        fields = ['player_goals', 'player_assist']

    def clean_player_goals(self):
        player_goals = self.cleaned_data['player_goals']
        if player_goals < 0:
            raise ValidationError("Goals must be equal to 0 or greater 0")
        return player_goals

    def clean_player_assist(self):
        player_assist = self.cleaned_data['player_assist']
        if player_assist < 0:
            raise ValidationError("Assist must be equal to 0 or greater 0")
        return player_assist


class Legend_story_Form(forms.ModelForm):
    legend_name = forms.CharField(max_length=30, label='Legend Name',
                                  required=True)
    legend_short_story = forms.CharField(max_length=50, label='Legend short Story', required=True)
    legend_roles = forms.CharField(max_length=50, label='Legend Roles', required=True)
    legend_inspiring = forms.CharField(max_length=100, label='Legend Inspiring', required=True)
    legend_quotes = forms.CharField(max_length=50, label='Legend Quotes', required=True)
    legend_image = forms.ImageField(label='Legend Image', required=True)

    class Meta:
        model = Legend_story
        fields = ['legend_name', 'legend_short_story', 'legend_roles', 'legend_inspiring', 'legend_quotes',
                  'legend_image']


class LiveMatchForm(forms.ModelForm):
    team1 = forms.CharField(max_length=30, label='Team 1',
                            required=True)
    team2 = forms.CharField(max_length=30, label='Team 2',
                            required=True)
    team1_score = forms.IntegerField(label='Team 1 Score', required=True)
    team2_score = forms.IntegerField(label='Team 2 Score', required=True)
    match_link = forms.URLField(label='Match Link', required=False)
    date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        label='Match Date',
        required=True
    )

    class Meta:
        model = Live_match
        fields = ['team1', 'team2', 'team1_score', 'team2_score', 'match_link', 'date']

    def clean_team1_score(self):
        team1_score = self.cleaned_data['team1_score']
        if team1_score < 0:
            raise ValidationError("Team score must be equal 0 or greater 0")
        return team1_score

    def clean_team2_score(self):
        team2_score = self.cleaned_data['team2_score']
        if team2_score < 0:
            raise ValidationError("Team score must be equal 0 or greater 0")
        return team2_score


class EditScoreForm(forms.ModelForm):
    team1_score = forms.IntegerField(label='Team 1 Score', required=True)
    team2_score = forms.IntegerField(label='Team 2 Score', required=True)

    class Meta:
        model = Live_match
        fields = ['team1_score', 'team2_score']

    def clean_team1_score(self):
        team1_score = self.cleaned_data['team1_score']
        if team1_score < 0:
            raise ValidationError("Team score must be equal 0 or greater 0")
        return team1_score

    def clean_team2_score(self):
        team2_score = self.cleaned_data['team2_score']
        if team2_score < 0:
            raise ValidationError("Team score must be equal 0 or greater 0")
        return team2_score


class CreateTrophyForm(forms.ModelForm):
    trophy_name = forms.CharField(max_length=20, label='Trophy Name', required=True)

    trophy_year = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        label='Trophy Year',
        required=True
    )

    class Meta:
        model = Trophy
        fields = ['trophy_name', 'trophy_year']
