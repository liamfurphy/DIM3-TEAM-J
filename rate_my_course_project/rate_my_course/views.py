import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, F
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from models import Course, Rating, University, UserProfile
from rate_my_course.forms import RatingForm, UserForm, UserProfileForm
from helpers import *
import datetime
import json


# FRONTEND VIEWS
def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    top5 = Course.objects.all().filter(average_overall__isnull=False).order_by('-average_overall')[:5]
    worst5 = Course.objects.all().filter(average_overall__isnull=False).order_by('average_overall')[:5]
    popular = Course.objects.all().order_by('-hits')[:5]

    return render_to_response('index.html', locals(), context)
	
	
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
			
			# Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)	

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
    next = None
    if "next" in request.GET:
        next = request.GET["next"]

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
                if next is not None:
                    return HttpResponseRedirect(next)
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

        return render_to_response('login.html', locals(), context)

@login_required
def profile(request):
    context = RequestContext(request)

    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    return render_to_response('profile.html', context)		

def results(request):
    context = RequestContext(request)
    return render_to_response('results.html', locals(), context)

def top_rated(request):
    context = RequestContext(request)
    return render_to_response('top.html', locals(), context)


def worst_rated(request):
    context = RequestContext(request)
    return render_to_response('worst.html', locals(), context)


def course(request, course_id):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    form = RatingForm(request.GET)
    try:
        c = Course.objects.get(id=int(course_id))
        c.hit()
        c.save()
    except:
        return HttpResponseRedirect('/')

    return render_to_response('course.html', locals(), context)


def uni(request, uni_id):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    try:
        u = University.objects.get(id=int(uni_id))
        courses = Course.objects.all().filter(uni=int(uni_id))
    except:
        return HttpResponseRedirect('/')

    return render_to_response('uni.html', locals(), context)


# API VIEWS
def api_get_latest(request, since=None):
    ticker = []
    if since is not None:
        latest_ratings = Rating.objects.all().order_by("-date").filter(date__range=(
        datetime.datetime.strptime(since, "%Y_%m_%d_%H_%M_%S") + datetime.timedelta(0, 1), datetime.datetime.now()))
        if len(latest_ratings) > 5:
            latest_ratings = latest_ratings[:5]
    else:
        latest_ratings = Rating.objects.all().order_by("-date")[:5]
    for r in latest_ratings:
        ticker.append({'datestr': r.date.strftime("%Y_%m_%d_%H_%M_%S"),
                       'username': r.user.user.username,
                       'classname': r.course.course_name,
                       'score': r.overall_rating})

    return HttpResponse(json.dumps(ticker), content_type="application/json")


def api_get_uni_courses(request, uni):
    results = build_course_list_for_api(courses = Course.objects.all().filter(uni=int(uni)))
    return HttpResponse(json.dumps(results), content_type="application/json")

def api_search_results(request, term):
    term = term.replace("_", " ")
    res = Course.objects.all().filter(
        Q(course_code__icontains=term) | Q(course_name__icontains=term) | Q(lecturer__name__icontains=term) | Q(
            uni__name__icontains=term))
    results = build_course_list_for_api(res)

    return HttpResponse(json.dumps(results), content_type="application/json")

def api_get_worst(request, amount):
    worst = Course.objects.all().filter(average_overall__isnull=False).order_by('average_overall')
    if len(worst) > amount:
        worst = worst[:amount]
    results = build_course_list_for_api(worst)

    return HttpResponse(json.dumps(results), content_type="application/json")

def api_get_top(request, amount):
    top = Course.objects.all().filter(average_overall__isnull=False).order_by('-average_overall')
    if len(top) > amount:
        worst = top[:amount]
    results = build_course_list_for_api(top)

    return HttpResponse(json.dumps(results), content_type="application/json")

def api_add_rating(request, course_id):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        results = []
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            rating = form.save(commit=False)
            rating.user = UserProfile.objects.get(id=int(request.user.id))
            rating.date = datetime.datetime.now()
            #try:
            c = Course.objects.get(id=int(course_id))
            rating.course = c

            rating.save()

            c.number_of_ratings += 1
            num = c.number_of_ratings
            c.average_difficulty = (c.average_difficulty * (num - 1) + int(form.cleaned_data['difficulty_rating'])) / (
            num)
            c.average_teaching = (c.average_teaching * (num - 1) + int(form.cleaned_data['teaching_rating'])) / (num)
            c.average_materials = (c.average_materials * (num - 1) + int(form.cleaned_data['materials_rating'])) / (num)
            c.average_overall = (c.average_overall * (num - 1) + int(form.cleaned_data['overall_rating'])) / (num)
            c.average_satisfaction = (c.average_satisfaction * (num - 1) + int(
                form.cleaned_data['satisfaction_rating'])) / (num)

            msg = {"data": {
                "overall": c.average_overall,
                "satisfaction": c.average_satisfaction,
                "difficulty": c.average_difficulty,
                "teaching": c.average_teaching,
                "materials": c.average_materials,
                "ratings": num
            }
            }
            results.append(msg)
            #except:
            #   return HttpResponseRedirect('/')
        else:
            print form.errors
            errors = {"errors": form.errors
                      #{ "overall": form.overall_rating.error_messages,
                      # "satisfaction_rating": form.satisfaction_rating.error_messages,
                      # "difficulty": form.difficulty_rating.error_messages,
                      # "teaching": form.teaching_rating.error_messages,
                      # "materials": form.materials_rating.error_messages,
                      # "comment": form.comment.error_messages}
            }
            results.append(errors)
        return HttpResponse(json.dumps(results), content_type="application/json")

    else:
        return course(request, course_id)
