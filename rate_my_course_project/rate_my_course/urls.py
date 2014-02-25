from django.conf.urls import patterns, url
from django.conf import settings
from rate_my_course import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^summary/course/(?P<course_id>\w+)/$', views.course, name='course'),
                       url(r'^summary/uni/(?P<uni_id>\w+)/$', views.uni, name='uni'),
                       )

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )