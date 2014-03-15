from django import forms
from django.db import models
from rate_my_course.models import Course, Rating

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