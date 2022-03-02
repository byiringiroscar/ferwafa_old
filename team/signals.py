from team.models import Team, Team_profile, Player, Player_profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Team)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Team_profile.objects.create(team=instance)
        print("profile created")


@receiver(post_save, sender=Team_profile)
def create_weeks(sender, instance, created, **kwargs):
    if created:
        print("profile_updated")


