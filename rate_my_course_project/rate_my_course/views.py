from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Course, Rating, Lecturer, University

def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    top5 = Course.objects.all().filter(average_overall__isnull=False).order_by('-average_overall')[:5]
    worst5 = Course.objects.all().filter(average_overall__isnull=False).order_by('average_overall')[:5]
    latest_ratings = Rating.objects.all().order_by("-date")[:5]

    return render_to_response('index.html', locals(), context)


def course(request, course_id):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    try:
        c = Course.objects.get(id=int(course_id))
    except:
        return HttpResponseRedirect('/')

    return render_to_response('course.html', locals(), context)


def uni(request, uni_id):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    try:
        u = University.objects.get(id=int(uni_id))
    except:
        return HttpResponseRedirect('/')

    return render_to_response('uni.html', locals(), context)
