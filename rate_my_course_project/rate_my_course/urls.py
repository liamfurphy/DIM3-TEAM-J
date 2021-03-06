from django.conf.urls import patterns, url
from django.conf import settings
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^results/$', views.results, name='results'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^logout/$', views.user_logout, name='user_logout'),
                       url(r'^confirm/(?P<confirmation_code>\w+)/(?P<username>\w+)/$', views.confirm, name='confirm'),
                       url(r'^summary/course/(?P<course_id>\w+)/$', views.course, name='course'),
                       url(r'^summary/uni/(?P<uni_id>\w+)/$', views.uni, name='uni'),
                       url(r'^top/$', views.top_rated, name='top'),
                       url(r'^worst/$', views.worst_rated, name='worst'),
                       url(r'^browse/$', views.browse, name='browse'),
                       url(r'^addcourse/$', views.add_course, name='addcourse'),

                       url(r'^get_uni_courses/$', views.get_uni_courses, name='get_uni_courses'),
                       url(r'^get_course_instances/$', views.get_course_instances, name='get_course_instances'),
                       url(r'^api/top/(?P<amount>\w+)/$', views.api_get_top, name='api_top'),
                       url(r'^api/worst/(?P<amount>\w+)/$', views.api_get_worst, name='api_worst'),
                       url(r'^api/courses/(?P<uni>\w+)/$', views.api_get_uni_courses, name='api_unis_courses'),
                       url(r'^api/add_course/$', views.api_add_course, name='api_add_course'),
                       url(r'^api/confirm/(?P<username>\w+)/$', views.api_resend_confirmation,
                           name='api_resend_confirmation'),
                       url(r'^api/get_lecturers/(?P<uni>\w+)/$', views.api_get_lecturers, name='api_get_lecturers'),
                       url(r'^api/results/(?P<term>\w+)/$', views.api_search_results, name='api_results'),
                       url(r'^api/rating/(?P<course_id>\w+)/$', views.api_add_rating, name='api_rating'),
                       url(r'^api/latest/(?P<since>\w+)/$', views.api_get_latest, name='api_latest'),
                       url(r'^api/latest/$', views.api_get_latest, name='api_latest'),
)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )