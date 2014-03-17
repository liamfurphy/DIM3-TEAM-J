from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    name = models.CharField(max_length=200)
    email_domain = models.CharField(max_length=50)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    telephone = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    is_email_verified = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=200)

	
    def __unicode__(self):
        return self.user.username
		
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Lecturer(models.Model):
    title = models.CharField(max_length=10,null=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    department = models.CharField(max_length=128, null=True, blank=True)
    uni = models.ForeignKey(University)
    def __unicode__(self):
        return "{0}. {1}".format(self.title, self.name)

class Course(models.Model):
    course_code = models.CharField(max_length=30)
    course_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    year_of_degree = models.IntegerField(null=True, blank=True)
    number_of_ratings = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)

    average_overall = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    average_difficulty = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    average_teaching = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    average_materials = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)
    average_satisfaction = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=1)

    lecturer = models.ForeignKey(Lecturer)
    uni = models.ForeignKey(University)

    def __unicode__(self):
        return self.course_name

    def hit(self):
        self.hits += 1


class Rating(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(UserProfile)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField()

    overall_rating = models.IntegerField()
    difficulty_rating = models.IntegerField()
    teaching_rating = models.IntegerField()
    materials_rating = models.IntegerField()
    satisfaction_rating = models.IntegerField()


    def __unicode__(self):
        return "{0}, rating {1}".format(self.course.course_code, self.id)


