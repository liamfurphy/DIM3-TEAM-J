from django import forms
from django.conf import settings
from django.core.mail import send_mail
from models import *

#helper for building a dict of course info to return as json
def build_course_list_for_api(courses):
    results = []
    for r in courses:
        o = {
            "course_id": r.id,
            "average_satisfaction": float(r.average_satisfaction if r.average_satisfaction else 0),
            "average_difficulty": float(r.average_difficulty if r.average_difficulty else 0),
            "average_materials": float(r.average_materials if r.average_materials else 0),
            "course_name": r.course_name,
            "description": r.description,
            "lecturer": r.lecturer.name,
            "average_teaching": float(r.average_teaching if r.average_teaching else 0),
            "number_of_ratings": r.number_of_ratings,
            "average_overall": float(r.average_overall if r.average_overall else 0),
            "uni": r.uni.name,
            "course_code": r.course_code,
            "year_of_degree": r.year_of_degree,
            "uni_id": r.uni.id}
        results.append(o)
    return results


def clean_passwords(self):
    password1 = self.cleaned_data.get('password')
    password2 = self.cleaned_data.get('conf_password')

    if not password2:
        raise forms.ValidationError("You must confirm your password")
    if password1 != password2:
        raise forms.ValidationError("Your passwords do not match")
    return password2


#helper to send verification emails
def send_registration_confirmation(request, user):
    title = "RateMyCourse Account Verification"
    content = "Hi, \nplease follow the following links to verify your email and be able to rate courses with RateMyCourse! \n\n" + \
              "http://" + request.get_host() + "/confirm/" + str(
        user.confirmation_code) + "/" + user.user.username + "\n\n" + \
              "Thanks, \n RateMyCourse Team."
    send_mail(title, content, settings.EMAIL_HOST_USER, [user.user.email], fail_silently=False)

# get all the lectuers for a university
def get_lec_choices(uni):
    choices = []
    m = Lecturer.objects.all().filter(uni=uni)
    for l in m:
        choices.append((l.id, l.name))

    choices.append((-1, "New Lecturer"))
    return choices



