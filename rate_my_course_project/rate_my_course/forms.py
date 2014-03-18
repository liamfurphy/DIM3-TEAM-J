from django import forms
from django.db import models
from models import Course, Rating, UserProfile, University, Lecturer
from django.contrib.auth.models import User


# Form used to add ratings to courses.
class RatingForm(forms.ModelForm):
    difficulty_rating = forms.ChoiceField(help_text="Difficulty Rating",
                                          choices=[(str(x), str(x)) for x in range(1, 11)],
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    teaching_rating = forms.ChoiceField(help_text="Teaching Rating",
                                        choices=[(str(x), str(x)) for x in range(1, 11)],
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    materials_rating = forms.ChoiceField(help_text="Materials Rating",
                                         choices=[(str(x), str(x)) for x in range(1, 11)],
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    satisfaction_rating = forms.ChoiceField(help_text="Satisfaction Rating",
                                            choices=[(str(x), str(x)) for x in range(1, 11)],
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    comment = forms.CharField(required=False,
                              max_length=200,
                              help_text="Comments",
                              widget=forms.Textarea(
                              attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Enter comments about the course'}))

    overall_rating = forms.ChoiceField(help_text="Overall Rating",
                                       choices=[(str(x), str(x)) for x in range(1, 11)],
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Rating
        exclude = ('user', 'date', 'course')

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'overall_rating',
            'difficulty_rating',
            'teaching_rating',
            'materials_rating',
            'satisfaction_rating',
            'comment']

#Form used for user registration
class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(help_text="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(help_text="Last Name", widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.CharField(help_text="Email Address", widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="Password")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


# Custom form so we dont display fields we dont want to
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()


# Form used for adding a course
class CourseForm(forms.ModelForm):
    course_code = forms.CharField(help_text="Course Code", widget=forms.TextInput(attrs={"class": "form-control"}))

    course_name = forms.CharField(help_text="Course Name", widget=forms.TextInput(attrs={"class": "form-control"}))

    description = forms.CharField(required=False,
                                  max_length=200,
                                  help_text="Course Description",
                                  widget=forms.Textarea(attrs={'rows': '4', "class": "form-control"}))

    year_of_degree = forms.IntegerField(help_text="Year of Degree", widget=forms.TextInput(attrs={"class": "form-control"}))

    uni = forms.ModelChoiceField(queryset=University.objects.all(),
                                 help_text="University",
                                 widget=forms.Select(attrs={"class": "form-control"}))

    lecturer = forms.ChoiceField(choices=[(-1, "Select University First")],
                                 help_text="Lecturer",
                                 widget=forms.Select(attrs={"class": "form-control"}))


    class Meta:
        model = Course
        exclude = ('number_of_ratings', 'hits', 'average_overall', 'average_difficulty', 'average_teaching',
                   'average_materials', 'average_satisfaction', 'lecturer')

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'uni',
            'course_name',
            'course_code',
            'year_of_degree',
            'lecturer',
            'description']

