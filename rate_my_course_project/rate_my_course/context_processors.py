# Context Processors we need during templating to help determine displayed content
from models import UserProfile


def can_add_course(request): # is the user able to add courses?
    return {'user_can_add_course': request.user.groups.filter(name='CourseAdders')}


def email_is_verified(request):
    try:
        return {'user_email_verified': UserProfile.objects.get(user=request.user).is_email_verified is True}
    except:
        return {'user_email_verified': False}
