from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from models import Course, Rating, University


def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    top5 = Course.objects.all().filter(average_overall__isnull=False).order_by('-average_overall')[:5]
    worst5 = Course.objects.all().filter(average_overall__isnull=False).order_by('average_overall')[:5]
    latest_ratings = Rating.objects.all().order_by("-date")[:5]

    return render_to_response('index.html', locals(), context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)
def results(request):
    context = RequestContext(request)
    errors = []
    res = None
    if request.method == 'GET':
        if 's' in request.GET:
            s = request.GET['s']
            res = Course.objects.all().filter(Q(course_code__icontains=s)|Q(course_name__icontains=s)|Q(lecturer__name__icontains=s)|Q(uni__name__icontains=s))
        else:
            errors.push("Search parameter was not provided")
    else:
        errors.push("Page was not accessed using HTTP GET")

    return render_to_response('results.html', locals(), context)

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
