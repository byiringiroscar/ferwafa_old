from django.shortcuts import get_object_or_404
from authentication.models import User_profile
from django.conf import settings

user = settings.AUTH_USER_MODEL


def extras(request):
    user = request.user
    if user.is_authenticated:
        user = request.user
        user_profile = User_profile.objects.get(user=user)

    else:
        user = None
        user_profile = None

    return {
        'user': user,
        'profile': user_profile,

    }
