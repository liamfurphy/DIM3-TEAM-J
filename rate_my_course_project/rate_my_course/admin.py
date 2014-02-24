from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import *


class UserInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserInline]

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_domain')
    search_fields = ['name', 'email_domain', 'country', 'city']

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'lecturer', 'uni')
    search_fields = ['course_code', 'course_name', 'lecturer', 'uni']


class LecturerAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'email')
    search_fields = ['first_name', 'last_name', 'email']

class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'user', 'date')
    search_fields = ['course', 'user']
    list_filter = ['date']


admin.site.register(University, UniversityAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Rating, RatingAdmin)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
