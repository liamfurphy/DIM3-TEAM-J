import os
from datetime import datetime

def populate():

    gu = add_uni("Glasgow University", "gla.ac.uk", "Scotland", "Glasgow", "")
    gcu = add_uni("Glasgow Caledonian University", "gcu.uk", "", "", "")
    edu = add_uni("University of Edinburgh", "ed.ac.uk", "Scotland", "Edinburgh", "")

    l1 = add_lecturer("Dr", "John", "Smith", "", "")
    l2 = add_lecturer("Dr", "Julie", "Smith", "julie@gla.ac.uk", "Mathematics")
    l3 = add_lecturer("Dr", "Julie", "Smith", "julie@gla.ac.uk", "Biology")

    u1 = add_user("jdoc", "jdoc@student.gla.ac.uk", "pass")
    u2 = add_user("jsmith", "jsmith@gla.ac.uk", "pass", True)
    u3 = add_user("bugs", "bbunny@student.gla.ac.uk", "pass")
    u4 = add_user("jblogs", "jblogs@student.gla.ac.uk", "pass")
    u5 = add_user("donduck", "dduck@student.gla.ac.uk", "pass")
    u6 = add_user("charizard", "charizard@student.gla.ac.uk", "pass")

    c1 = add_course(code="CS1P", name="Introduction to Programming", avg_overall=50, avg_difficulty=50, avg_materials=50, avg_satisfaction=50,
                    avg_teaching=50, numratings=2, year=1, lecturer=l1, uni=gu)

    c2 = add_course(code="CS1Q", name="Introduction to Non Programming", avg_overall=50, avg_difficulty=50, avg_materials=50, avg_satisfaction=50,
                    avg_teaching=50, numratings=1, year=1, lecturer=l2, uni=gu)

    c3 = add_course(code="CS3X", name="DIM3", avg_overall=50, avg_difficulty=50, avg_materials=50, avg_satisfaction=50,
                    avg_teaching=50, numratings=1, year=3, lecturer=l2, uni=gu)

    c4 = add_course(code="CS3Y", name="OS3", avg_overall=50, avg_difficulty=50, avg_materials=50, avg_satisfaction=50,
                    avg_teaching=50, numratings=1, year=3, lecturer=l1, uni=gu)

    c5 = add_course(code="CS3Z", name="NS3", avg_overall=50, avg_difficulty=50, avg_materials=50, avg_satisfaction=50,
                    avg_teaching=50, numratings=1, year=3, lecturer=l2, uni=gu)

    c6 = add_course(code="BIO4", name="Biology 4", numratings=0, year=4, lecturer=l3, uni=gcu)

    r1 = add_rating(c1, u1, datetime.now(), 0, 0 ,0, 0, 0, "BAD COURSE - bloody terrible")
    r2 = add_rating(c1, u3, datetime.now(), 100, 100 ,100, 100, 100, "This is possibly the greatest course in the history of mankind")

    r3 = add_rating(c2, u1, datetime.now(), 50, 50 ,50, 50, 50)
    r7 = add_rating(c2, u3, datetime.now(), 50, 50 ,50, 50, 50)
    r8 = add_rating(c2, u4, datetime.now(), 50, 50 ,50, 50, 50)

    r4 = add_rating(c3, u1, datetime.now(), 50, 50 ,50, 50, 50)
    r5 = add_rating(c3, u5, datetime.now(), 50, 50 ,50, 50, 50)
    r6 = add_rating(c3, u4, datetime.now(), 50, 50 ,50, 50, 50)

    r9 = add_rating(c4, u6, datetime.now(), 50, 50 ,50, 50, 50)
    r10 = add_rating(c4, u5, datetime.now(), 50, 50 ,50, 50, 50)
    r11 = add_rating(c4, u4, datetime.now(), 50, 50 ,50, 50, 50)

    r12 = add_rating(c5, u4, datetime.now(), 50, 50 ,50, 50, 50)
    r13 = add_rating(c5, u6, datetime.now(), 50, 50 ,50, 50, 50)
    r14 = add_rating(c5, u1, datetime.now(), 50, 50 ,50, 50, 50)


def add_uni(name, email, country=None, city=None, tel=None) :
    u = University.objects.get_or_create(name=name, email_domain=email, country=country, city=city, telephone=tel)[0]
    return u

def add_user(username, email, password, can_add_course=False):
    u = User.objects.get_or_create(username=username, email=email, password=password)[0]
    u.save()
    if can_add_course:
        g = Group.objects.get_or_create(name="CourseAdders")[0]
        g.user_set.add(u)
    up = UserProfile()
    up.user = u
    up.save()
    return up

def add_lecturer(title, name, last_name, email=None, dept=None):
    l = Lecturer.objects.get_or_create(title=title, first_name=name, last_name=last_name, email=email, department=dept)[0]
    return l

def add_course(code, name, numratings, lecturer, uni, avg_overall=None, avg_difficulty=None, avg_teaching=None, avg_materials=None, avg_satisfaction=None, year=None, desc=None):
    c = Course.objects.get_or_create(course_code=code, course_name=name, year_of_degree=year, description=desc, number_of_ratings=numratings, average_overall=avg_overall, average_difficulty=avg_difficulty,
                                     average_teaching=avg_teaching, average_materials=avg_materials, average_satisfaction=avg_satisfaction, lecturer=lecturer, uni=uni)[0]
    return c

def add_rating(course, user, date, overall, difficulty, teaching, materials, satisfaction, comment=None):
    r = Rating.objects.get_or_create(course=course, user=user, comment=comment, date=date, overall_rating=overall, difficulty_rating=difficulty, teaching_rating=teaching,
                                     materials_rating=materials, satisfaction_rating=satisfaction)[0]
    return r


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_my_course_project.settings')
    from rate_my_course.models import *
    from django.contrib.auth.models import User, Group
    populate()