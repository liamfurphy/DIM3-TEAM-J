def can_add_course(request):
    return { 'user_can_add_course' : request.user.groups.filter(name='CourseAdders') }