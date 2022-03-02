from authentication.models import User, User_profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from team.models import Player, Player_profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User_profile.objects.create(user=instance)
        print("profile created")


@receiver(post_save, sender=User_profile)
def create_weeks(sender, instance, created, **kwargs):
    if created:
        print("profile_updated")


@receiver(post_save, sender=Player)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        Player_profile.objects.create(player=instance)
        print("player profile created")