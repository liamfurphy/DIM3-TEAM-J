from django import forms
from django.db import models
from rate_my_course.models import Course, Rating, UserProfile, University, Lecturer
from django.contrib.auth.models import User

class RatingForm(forms.ModelForm):
    overall_rating = forms.IntegerField(help_text="Course overall: ")
    difficulty_rating = forms.IntegerField(help_text="Course difficulty: ")
    teaching_rating = forms.IntegerField(help_text="Course teaching: ")
    materials_rating = forms.IntegerField(help_text="Course materials: ")
    satisfaction_rating = forms.IntegerField(help_text="Course satisfaction: ")
    comment = forms.CharField(max_length=200, help_text="Comment about the course: ",
                              widget=forms.Textarea(attrs={'rows': '4'}))
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
			
class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    first_name = forms.CharField(help_text="Please enter a first name.")
    last_name = forms.CharField(help_text="Please enter your last name.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password')
	
class UserProfileForm(forms.ModelForm):
	
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}), help_text="Please enter your date of birth.")
	
    class Meta:
		model = UserProfile
		fields = ('date_of_birth',)
        
class CourseForm(forms.ModelForm):
    course_code = forms.CharField(help_text="Course Code: ")
    course_name = forms.CharField(help_text="Course Name: ")
    description = forms.CharField(required=False, max_length=200, help_text="Course description: ",
                              widget=forms.Textarea(attrs={'rows': '4'}))
    year_of_degree = forms.IntegerField(help_text="Enter year fo degree: ")
    uni = forms.ModelChoiceField(queryset=University.objects.all(),help_text="Select a university: ")
    lecturer = forms.ChoiceField(choices=[(-1,"-----------")],help_text="Select a lecturer: ")

    class Meta:
        model = Course
        exclude = ('number_of_ratings','hits','average_overall','average_difficulty','average_teaching',
                                            'average_materials', 'average_satisfaction')

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
                'uni',
                'course_name',
                'course_code',
                'year_of_degree',
                'lecturer',
                'description']

