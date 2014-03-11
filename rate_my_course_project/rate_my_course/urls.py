from django.conf.urls import patterns, url
from django.conf import settings
from rate_my_course import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^results/$', views.results, name='results'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='user_logout'),
                       url(r'^summary/course/(?P<course_id>\w+)/$', views.course, name='course'),
                       url(r'^summary/uni/(?P<uni_id>\w+)/$', views.uni, name='uni'),
                       url(r'^api/results/(?P<term>\w+)/$', views.api_search_results, name='api_results'),
                       url(r'^api/rating/(?P<course_id>\w+)/$', views.api_add_rating, name='api_rating')
                       )

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )