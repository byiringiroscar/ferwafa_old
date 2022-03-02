from django.contrib import admin
from team.models import Team, Team_profile, Player, Player_profile, Ranking_Table, Table_Ranking, Trophy, Trophy_team, \
     player_statistics_ranking, Live_match, Legend_story


# Register your models here.
class Table_RankingAdmin(admin.ModelAdmin):
    readonly_fields = ('team_points', 'game_played',)


admin.site.register(Team)
admin.site.register(Team_profile)
admin.site.register(Player)
admin.site.register(Player_profile)
admin.site.register(Ranking_Table)
admin.site.register(Table_Ranking, Table_RankingAdmin)
admin.site.register(Trophy)
admin.site.register(Trophy_team)
admin.site.register(player_statistics_ranking)
admin.site.register(Live_match)
admin.site.register(Legend_story)
