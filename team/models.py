from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

now = timezone.now()
today_year_exact = datetime.date.today()

User = settings.AUTH_USER_MODEL


# Create your models here.


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    team_name = models.CharField(max_length=50)
    team_picture = models.ImageField(upload_to='images/', default='team_logo.png')
    team_president = models.CharField(max_length=100)
    player = models.ManyToManyField('Player')

    def __str__(self):
        return f'{self.team_name} {self.team_president}'

    class Meta:
        verbose_name_plural = "Team"
        ordering = ['-id']


class Team_profile(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    team_stadium = models.CharField(max_length=100, blank=True, null=True)
    team_location = models.CharField(max_length=100, blank=True, null=True)
    team_founded = models.DateTimeField(blank=True, null=True)
    team_contact = models.EmailField(blank=True, null=True)
    team_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.team.team_name} {self.team_contact}'

    class Meta:
        verbose_name_plural = "Team_profile"
        ordering = ['-id']


# player model
class Player(models.Model):
    position = [
        ('striker', 'striker'),
        ('goalkeeper', 'goalkeeper'),
        ('left_winger', 'left_winger'),
        ('right_winger', 'right_winger'),
        ('fullback', 'fullback'),
        ('wingback', 'wingback'),
        ('centre_back', 'centre_back'),
        ('attacking_midfielder', 'attacking_midfielder'),
        ('defensive_midfielder', 'defensive_midfielder'),
        ('centre_midfielder', 'centre_midfielder'),
    ]
    player_name = models.CharField(max_length=100)
    player_number = models.PositiveIntegerField()
    player_position = models.CharField(max_length=200, choices=position)
    player_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.player_name}'

    class Meta:
        verbose_name_plural = "Player"
        ordering = ['-id']


class Player_profile(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    player_height = models.CharField(max_length=50, blank=True, null=True)
    player_born = models.DateTimeField(blank=True, null=True, default=today_year_exact)
    player_age = models.CharField(max_length=100, blank=True, null=True)
    player_contact = models.EmailField(max_length=100, blank=True, null=True)
    player_link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        today_year = datetime.date.today().year
        player_born_year = self.player_born.year
        age_player = today_year - player_born_year
        self.player_age = age_player
        super(Player_profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.player.player_name}'

    class Meta:
        verbose_name_plural = "Player_profile"
        ordering = ['-id']


# team ranking
class Ranking_Table(models.Model):
    ranking_year = models.DateField()
    ranking_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.ranking_name} -- {self.ranking_year}'

    class Meta:
        verbose_name_plural = "Ranking_year"
        ordering = ['-id']


class Table_Ranking(models.Model):
    ranking = models.ForeignKey(Ranking_Table, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    win = models.PositiveIntegerField(blank=True, null=True, default=0)
    draw = models.PositiveIntegerField(blank=True, null=True, default=0)
    loss = models.PositiveIntegerField(blank=True, null=True, default=0)
    team_points = models.PositiveIntegerField(blank=True, null=True)
    game_played = models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.team.team_name} -- {self.ranking.ranking_year}'

    def save(self, *args, **kwargs):
        win = self.win * 3
        loss = self.loss * 0
        draw = self.draw * 1
        self.team_points = win + loss + draw
        self.game_played = self.win + self.loss + self.draw
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Table_Ranking"
        ordering = ['-team_points']


# end team ranking

# trophy team
class Trophy(models.Model):
    trophy_name = models.CharField(max_length=40)
    trophy_year = models.DateField()

    def __str__(self):
        return f'{self.trophy_name} -- {self.trophy_year}'

    class Meta:
        verbose_name_plural = "Trophy"
        ordering = ['-id']


class Trophy_team(models.Model):
    trophy = models.ForeignKey(Trophy, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    trophy_image = models.ImageField(default='cup.png')

    def __str__(self):
        return f'{self.team.team_name} -- {self.trophy.trophy_name}'

    class Meta:
        verbose_name_plural = "Trophy Team"
        ordering = ['-id']


# end of trophy
# player goal and assist sections
class player_statistics_ranking(models.Model):
    player_year_statistics = models.ForeignKey(Ranking_Table, on_delete=models.SET_NULL, null=True)
    player_statistics = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    player_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player_goals = models.PositiveIntegerField(default=0)
    player_assist = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.player_statistics.player_name}--Goals---{self.player_goals}--assist-----{self.player_assist}--year-----{self.player_year_statistics.ranking_year} '

    class Meta:
        verbose_name_plural = "player_statistics_Ranking"
        ordering = ['-id']


# end goals and assist party

# live match

class Live_match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
    match_link = models.URLField()
    date = models.DateTimeField()
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.team1}----VS----{self.team2}'

    class Meta:
        verbose_name_plural = "Live_match"
        ordering = ['-id']


class Legend_story(models.Model):
    legend_name = models.CharField(max_length=50)
    legend_short_story = models.TextField()
    legend_roles = models.CharField(max_length=50)
    legend_inspiring = models.CharField(max_length=100)
    legend_quotes = models.CharField(max_length=50)
    legend_image = models.ImageField(upload_to='images/', default='coach.png')

    def __str__(self):
        return f'{self.legend_name}'

    class Meta:
        verbose_name_plural = "Legend_story"
        ordering = ['-id']
