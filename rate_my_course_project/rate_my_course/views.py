import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from models import Course, Rating, University, UserProfile, Lecturer
from forms import RatingForm, UserForm, UserProfileForm, CourseForm
from helpers import *
from decimal import *

import datetime
import string
import random
import json


def encode_url(url):
    return url.replace(" ", "_")


def decode_url(url):
    return url.replace("_", " ")


# FRONTEND VIEWS
def index(request):
    context = RequestContext(request)

    top5 = Course.objects.all().filter(average_overall__isnull=False).order_by('-average_overall')[:5]
    worst5 = Course.objects.all().filter(average_overall__isnull=False).order_by('average_overall')[:5]
    popular = Course.objects.all().order_by('-hits')[:5]

    return render_to_response('index.html', locals(), context)


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # check that the users domain
            # matches one kept in out DB
            # this python hack gets around the fact that uni domains are often substring
            # of student emails. (since we want lectures to be able to register with having
            # different fields or duplicate universities
            domains = [d for d in University.objects.all() if d.email_domain in user.email.split("@")[1]]
            if len(domains) < 1:
                return HttpResponse("Your email domain is invalid.")

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.confirmation_code = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(100))

            profile.save()

            #send the verification email
            send_registration_confirmation(request, profile)

            registered = True
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            login(request, user)

        else:
            print user_form.errors, profile_form.errors


    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'register.html', locals(), context)


#View for confirming users email
def confirm(request, confirmation_code, username):
    context = RequestContext(request)
    username = username
    success = False
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        if profile.confirmation_code == confirmation_code:
            profile.is_email_verified = True
            profile.save()
            success = True
    except:
        pass #success stays false so do nothing
    return render_to_response(
        'confirm.html',
        locals(),
        context)


@login_required
def user_logout(request):
    print "HERE"
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    context = RequestContext(request)
    next = None # what page will we go to once we've logged in?

    if "next" in request.GET:
        next = request.GET["next"]

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if next is not None:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect('/')
            else:
                disabled_account = True
                return render_to_response('login.html', locals(), context)
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            bad_details = True
            return render_to_response('login.html', locals(), context)


    else:
        return render_to_response('login.html', locals(), context)


@login_required
def profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['conf_password']
        if password1 == password2:
            user.set_password('password')
        else:
            print "Passwords did match: {0}, {1}".format(password1, password2)
            Not_matched = True
            return render_to_response('profile.html', locals(), context_instance=RequestContext(request))

        user.save()
        return HttpResponseRedirect('/profile/')

    user_profile = request.user.get_profile()
    return render_to_response('profile.html',
                              locals(), context_instance=RequestContext(request))

#The following 3 Pages are ajax driven and thus have simple empty views
def results(request):
    context = RequestContext(request)
    return render_to_response('results.html', locals(), context)


def top_rated(request):
    context = RequestContext(request)
    return render_to_response('top.html', locals(), context)


def worst_rated(request):
    context = RequestContext(request)
    return render_to_response('worst.html', locals(), context)

# Summary view for a course.
def course(request, course_id):
    context = RequestContext(request)
    form = RatingForm(request.GET)
    if request.user.is_authenticated():
        submitted = Rating.objects.filter(course=Course.objects.get(id=int(course_id)),
                                          user=UserProfile.objects.get(user=int(request.user.id))).exists()
    else:
        submitted = False
    try:
        c = Course.objects.get(id=int(course_id))
        c.hit()
        c.save()
        ratings = Rating.objects.all().filter(course=int(course_id))
    except:
        #course doesnt exist? Back to homepage then
        return HttpResponseRedirect('/')

    return render_to_response('course.html', locals(), context)

#Summary view for unis
def uni(request, uni_id):
    context = RequestContext(request)
    try:
        u = University.objects.get(id=int(uni_id))
        courses = Course.objects.all().filter(uni=int(uni_id))
    except:
        #doestn exist, back to homepage
        return HttpResponseRedirect('/')

    return render_to_response('uni.html', locals(), context)

#page for course adding
def add_course(request):
    context = RequestContext(request)
    print request.user.groups.filter(name='CourseAdders')
    if request.user.is_authenticated() == True and request.user.groups.filter(name='CourseAdders').exists():
        form = CourseForm(request.GET)
        return render_to_response('add_course.html', locals(), context)
    else:
        return HttpResponseRedirect('/')


# API VIEWS

#get the latest ratings, if since is given the only return ratings since the date provided
def api_get_latest(request, since=None):
    results = []
    if since is not None:
        latest_ratings = Rating.objects.all().order_by("-date").filter(date__range=(
            datetime.datetime.strptime(since, "%Y_%m_%d_%H_%M_%S") + datetime.timedelta(0, 1), datetime.datetime.now()))
        if len(latest_ratings) > 5:
            latest_ratings = latest_ratings[:5]
    else:
        latest_ratings = Rating.objects.all().order_by("-date")[:5]
    for r in latest_ratings:
        results.append({'datestr': r.date.strftime("%Y_%m_%d_%H_%M_%S"),
                        'username': r.user.user.username,
                        'classname': r.course.course_name,
                        'score': r.overall_rating})

    return HttpResponse(json.dumps(results), content_type="application/json")


# get the courses for a university
def api_get_uni_courses(request, uni):
    results = build_course_list_for_api(courses=Course.objects.all().filter(uni=int(uni)))
    return HttpResponse(json.dumps(results), content_type="application/json")

#get lecturers of a uni
def api_get_lecturers(request, uni):
    return HttpResponse(json.dumps(get_lec_choices(uni)), content_type="application/json")

# get the results of a particular search, not the most complex search, just a bunch of like queries
def api_search_results(request, term):
    term = term.replace("_", " ")
    res = Course.objects.all().filter(
        Q(course_code__icontains=term) | Q(course_name__icontains=term) | Q(lecturer__name__icontains=term) | Q(
            uni__name__icontains=term))
    results = build_course_list_for_api(res)
    return HttpResponse(json.dumps(results), content_type="application/json")

#get the worst amount courses
def api_get_worst(request, amount):
    worst = Course.objects.all().filter(average_overall__isnull=False).order_by('average_overall')
    if len(worst) > amount:
        worst = worst[:amount]
    results = build_course_list_for_api(worst)

    return HttpResponse(json.dumps(results), content_type="application/json")

#ge the top amount courses
def api_get_top(request, amount):
    top = Course.objects.all().filter(average_overall__isnull=False).order_by('-average_overall')
    if len(top) > amount:
        worst = top[:amount]
    results = build_course_list_for_api(top)

    return HttpResponse(json.dumps(results), content_type="application/json")

#add a rating for courseID
def api_add_rating(request, course_id):
    context = RequestContext(request)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        results = []

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = UserProfile.objects.get(user=int(request.user.id))
            rating.date = datetime.datetime.now()
            try:
                c = Course.objects.get(id=int(course_id))
                rating.course = c
                rating.save()

                #update the course averages
                c.number_of_ratings += 1
                c.average_difficulty = ((c.average_difficulty if c.average_difficulty else 0) * (
                    c.number_of_ratings - 1) + Decimal(form.cleaned_data['difficulty_rating'])) \
                                       / Decimal(c.number_of_ratings)

                c.average_teaching = ((c.average_teaching if c.average_teaching else 0) * (
                    c.number_of_ratings - 1) + Decimal(form.cleaned_data['teaching_rating'])) \
                                     / Decimal(c.number_of_ratings)

                c.average_materials = ((c.average_materials if c.average_materials else 0) * (c.number_of_ratings - 1) +
                                       Decimal(form.cleaned_data['materials_rating'])) / Decimal(c.number_of_ratings)

                c.average_overall = ((c.average_overall if c.average_overall else 0) * (
                    c.number_of_ratings - 1) + Decimal(form.cleaned_data['overall_rating'])) \
                                    / Decimal(c.number_of_ratings)

                c.average_satisfaction = ((c.average_satisfaction if c.average_satisfaction else 0) * (
                    c.number_of_ratings - 1) + Decimal(form.cleaned_data['satisfaction_rating'])) \
                                         / Decimal(c.number_of_ratings)

                c.save()

                #response contains averages for the course, and the username of the submitter
                msg = {"data": {
                    "overall": float(c.average_overall),
                    "satisfaction": float(c.average_satisfaction),
                    "difficulty": float(c.average_difficulty),
                    "teaching": float(c.average_teaching),
                    "materials": float(c.average_materials),
                    "ratings": c.number_of_ratings,
                    "username": request.user.username
                }
                }
                results.append(msg)
            except Exception as e:
                return HttpResponseRedirect('/')
        else:
            print form.errors
            errors = {"errors": form.errors
            }
            results.append(errors)
        print "Going to return"
        return HttpResponse(json.dumps(results), content_type="application/json")

    else:
        return course(request, course_id)


#api endpoint to add a course
def api_add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            c = form.save(commit=False)

            if int(request.POST["lecturer"]) == -1:

                lec = Lecturer(title=request.POST["lecturer_title"],
                               name=request.POST["lecturer_name"],
                               department=request.POST["lecturer_dept"],
                               email=request.POST["lecturer_email"],
                               uni=University.objects.get(id=int(request.POST["uni"])))
                lec.save()
                c.lecturer = lec

            else:
                c.lecturer = form.lecturer
            c.save()

            return course(request, c.id)
        else:
            print form.errors
            return add_course(request)
    return add_course(request)


def api_resend_confirmation(request, username):
    send_registration_confirmation(request, UserProfile.objects.get(user=User.objects.get(username=username)))
    return HttpResponse("Resent!")


def browse(request):
    # Get the context of the HTTP
    context = RequestContext(request)
    # Ger all the univeristies list for choosing
    Universities = University.objects.all()
    for univ in Universities:
        univ.url = encode_url(univ.name)
        univ.course_num = len(Course.objects.all().filter(uni=univ))
    return render_to_response("browse.html", locals(), context)


def get_uni_courses(request):
    context = RequestContext(request)
    uni_name = request.GET['university']
    uniID = University.objects.get(name=uni_name)
    courses = Course.objects.all().filter(uni=uniID)
    for course in courses:
        course.url = encode_url(course.course_name)
    return render_to_response('course_list.html', locals(), context)


def get_course_instances(request):
    context = RequestContext(request)
    c_name = request.GET['course']
    uni_name = request.GET['university']
    university = University.objects.get(name=uni_name)
    courseID = Course.objects.get(course_name=c_name)
    c = Course.objects.get(course_name=courseID, uni=university)
    c.course_name = encode_url(c_name)
    top_good_reviews = Rating.objects.all().filter(overall_rating__isnull=False, course=courseID).order_by(
        '-overall_rating')[:3]
    top_worst_reviews = Rating.objects.all().filter(overall_rating__isnull=False, course=courseID).order_by(
        'overall_rating')[:3]
    return render_to_response('final_list.html', locals(), context)


def get_lec_choices(uni):
    choices = []
    m = Lecturer.objects.all().filter(uni=uni)
    for l in m:
        choices.append((l.id, l.name))

    choices.append((-1, "New Lecturer"))
    return choices



