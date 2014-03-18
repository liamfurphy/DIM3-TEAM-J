# Context Processors we need during templating to help determine displayed content

def can_add_course(request): # is the user able to add courses?
    return {'user_can_add_course': request.user.groups.filter(name='CourseAdders')}
