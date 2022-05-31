from django.shortcuts import get_object_or_404
from authentication.models import User_profile
from django.conf import settings
from team.models import Connect_message

user = settings.AUTH_USER_MODEL


def extras(request):
    user = request.user
    notification_message = Connect_message.objects.filter(team__user=user, readed_message=False).order_by('-date')[:5]


    if user.is_authenticated:

        user = request.user
        user_profile = User_profile.objects.get(user=user)
        if notification_message.exists():
            notification_message = Connect_message.objects.filter(team__user=user, readed_message=False).order_by(
                '-date')[:5]
            notification = notification_message.count()
        else:
            notification = 0
            notification_message = []

    else:
        user = None
        user_profile = None
        notification = 0

    return {
        'user': user,
        'profile': user_profile,
        'notification_message': notification_message,
        'notification': notification,

    }
