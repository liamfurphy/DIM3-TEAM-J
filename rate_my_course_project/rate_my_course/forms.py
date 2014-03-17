from django import forms
from django.db import models
from rate_my_course.models import Course, Rating
from rate_my_course.models import UserProfile
from django.contrib.auth.models import User

class RatingForm(forms.ModelForm):
    difficulty_rating = forms.ChoiceField(help_text="Difficulty Rating",  choices = [(str(x), str(x)) for x in range(1,11)], widget = forms.Select(attrs={'class': 'form-control'}))
    teaching_rating = forms.ChoiceField(help_text="Teaching Rating",  choices = [(str(x), str(x)) for x in range(1,11)], widget = forms.Select(attrs={'class': 'form-control'}))
    materials_rating = forms.ChoiceField(help_text="Materials Rating",  choices = [(str(x), str(x)) for x in range(1,11)], widget = forms.Select(attrs={'class': 'form-control'}))
    satisfaction_rating = forms.ChoiceField(help_text="Satisfaction Rating",  choices = [(str(x), str(x)) for x in range(1,11)], widget = forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(required=False, max_length=200, help_text="Comments", widget=forms.Textarea(attrs={'rows' : 5, 'class': 'form-control', 'placeholder': 'Enter comments about the course'}))
    overall_rating = forms.ChoiceField(help_text= "Overall Rating", choices = [(str(x), str(x)) for x in range(1,11)], widget = forms.Select(attrs={'class': 'form-control'}))

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
        
