import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, F
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers

from models import Course, Rating, University, UserProfile, Lecturer
from rate_my_course.forms import RatingForm, UserForm, UserProfileForm, CourseForm
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

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
            user = user_form.save()

            domains = [d for d in University.objects.all() if d.email_domain in user.email.split("@")[1]]
            if len(domains) < 1:
                return HttpResponse("Your email domain is invalid.")
                # Save the user's form data to the database.

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.confirmation_code = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(100))

            # Now we save the UserProfile model instance.
            profile.save()
            send_registration_confirmation(request, profile)

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


def send_registration_confirmation(request, user):
    title = "RateMyCourse account confirmation"
    content = "http://" + request.get_host() + "/confirm/" + str(user.confirmation_code) + "/" + user.user.username
    send_mail(title, content, settings.EMAIL_HOST_USER, [user.user.email], fail_silently=False)


def confirm(request, confirmation_code, username):
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        if profile.confirmation_code == confirmation_code:
            profile.is_email_verified = True
            profile.save()
            return HttpResponse("Confirmed!")
        return HttpResponseRedirect("Not Confirmed")
    except:
        return HttpResponseRedirect('../../../../../')

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
    
    context_dict = {}
	
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
                context_dict['disabled_account'] = True
                return render_to_response('login.html', context_dict, context)
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('login.html', context_dict, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...

        return render_to_response('login.html', locals(), context)


@login_required
def profile(request):
    success = False
    u = User.objects.get(id=1)

    if request.method == 'POST':
        upform = UserProfileForm(request.POST, instance=u.profile)
        if upform.is_valid():
            up = upform.save(commit=False)
            up.user = request.user
            up.save()
            success = True
    else:
        upform = UserProfileForm(instance=u.profile)

    return render_to_response('profile.html',
                              locals(), context_instance=RequestContext(request))


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
    results = build_course_list_for_api(courses=Course.objects.all().filter(uni=int(uni)))
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
            rating.user = UserProfile.objects.get(user=int(request.user.id))
            rating.date = datetime.datetime.now()
            try:
                c = Course.objects.get(id=int(course_id))
                rating.course = c

                rating.save()

                num = c.number_of_ratings
                if num is None:
                    num = 0
                c.number_of_ratings = num + 1
                num = num + 1
                c.average_difficulty = ((c.average_difficulty if c.average_difficulty else 0) * (num - 1) +
                                        Decimal(form.cleaned_data['difficulty_rating'])) / Decimal(num)
                c.average_teaching = ((c.average_teaching if c.average_teaching else 0) * (num - 1) +
                                      Decimal(form.cleaned_data['teaching_rating'])) / Decimal(num)
                c.average_materials = ((c.average_materials if c.average_materials else 0) * (num - 1) +
                                       Decimal(form.cleaned_data['materials_rating'])) / Decimal(num)
                c.average_overall = ((c.average_overall if c.average_overall else 0) * (num - 1) +
                                     Decimal(form.cleaned_data['overall_rating'])) / Decimal(num)
                c.average_satisfaction = ((c.average_satisfaction if c.average_satisfaction else 0) * (num - 1) +
                                          Decimal(form.cleaned_data['satisfaction_rating'])) / Decimal(num)

                c.save()

                msg = {"data": {
                    "overall": float(c.average_overall),
                    "satisfaction": float(c.average_satisfaction),
                    "difficulty": float(c.average_difficulty),
                    "teaching": float(c.average_teaching),
                    "materials": float(c.average_materials),
                    "ratings": num,
                    "username": request.user.username
                }
                }
                results.append(msg)
            except Exception as e:
                print e.message
                import traceback

                traceback.print_exc()
                raise e
                return HttpResponseRedirect('/')
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
        print "Going to return"
        return HttpResponse(json.dumps(results), content_type="application/json")

    else:
        return course(request, course_id)


def api_add_course(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        results = []
        # Have we been provided with a valid form?
        if form.is_valid():
            c = form.save(commit=False)
            if int(request.POST["lecturer"])==-1:

                lec = Lecturer(name=request.POST["lecturer_name"],
                                     uni=University.objects.get(id=int(request.POST["uni"])))
                lec.save()
                c.lecturer = lec
            else:
                c.lecturer = form.lecturer
            print c.lecturer.name
            print c.lecturer.id
            c.save()

            return course(request, c.id)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
            return add_course(request)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CourseForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return add_course(request)


def api_get_lecturers(request, uni):
    return HttpResponse(json.dumps(get_lec_choices(uni)), content_type="application/json")


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


def add_course(request):
    context = RequestContext(request)
    # Obtain the context from the HTTP request.
    form = CourseForm(request.GET)
    #return api_add_course(request)
    return render_to_response('add_course.html', locals(), context)
