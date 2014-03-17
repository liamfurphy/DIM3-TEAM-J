import os
from datetime import datetime

def populate():

    gu = add_uni("Glasgow University", "gla.ac.uk", "Scotland", "Glasgow", "")
    gcu = add_uni("Glasgow Caledonian University", "gcu.uk", "", "", "")
    edu = add_uni("University of Edinburgh", "ed.ac.uk", "Scotland", "Edinburgh", "")

    l1 = add_lecturer("Dr", "Leif Azzopardi", "Leif.Azzopardi@glasgow.ac.uk", "Computing Science")
    l2 = add_lecturer("Dr", "Jonathan Nimmo", "jnimmo@glasgow.ac.uk", "Mathematics")
    l3 = add_lecturer("Dr", "Colin Perkins", "colin.perkins@gla.ac.uk", "Computing Science")
    l4 = add_lecturer("Dr", "Joe Sventek", "joe@gla.ac.uk", "Computing Science")

    u1 = add_user("jdoc", "jdoc@student.gla.ac.uk", "pass", first_name="John", last_name="Docherty")
    u2 = add_user("leifos", "Leif.Azzopardi@glasgow.ac.uk", "pass", can_add_course=True, first_name="Leif", last_name="Azzopardi")
    u3 = add_user("bugs", "bbunny@student.gla.ac.uk", "pass", first_name="Bugs", last_name="Bunny")
    u4 = add_user("jblogs", "jblogs@student.gla.ac.uk", "pass", first_name="Joe", last_name="Blogs")
    u5 = add_user("donduck", "dduck@student.gla.ac.uk", "pass", first_name="Donald", last_name="Duck")
    u6 = add_user("charizard", "charizard@student.gla.ac.uk", "pass")

    c1 = add_course(code="CS1P", name="Introduction to Programming", avg_overall=7, avg_difficulty=5, avg_materials=3, avg_satisfaction=4,
                    avg_teaching=10, numratings=2, year=1, lecturer=l1, uni=gu, hits=40)

    c2 = add_course(code="CS1Q", name="Introduction to Non Programming", avg_overall=4, avg_difficulty=4, avg_materials=4, avg_satisfaction=4,
                    avg_teaching=4, numratings=3, year=1, lecturer=l4, uni=edu, hits=2)

    c3 = add_course(code="CS3X", name="DIM3", avg_overall=9, avg_difficulty=9, avg_materials=9, avg_satisfaction=9,
                    avg_teaching=9, numratings=3, year=3, lecturer=l1, uni=gu, hits=12)

    c4 = add_course(code="MATH1R", name="Maths 1R", avg_overall=3, avg_difficulty=3, avg_materials=3, avg_satisfaction=3,
                    avg_teaching=3, numratings=3, year=1, lecturer=l2, uni=gu, hits=33)

    c5 = add_course(code="CS3Z", name="NS3", avg_overall=1, avg_difficulty=2, avg_materials=6, avg_satisfaction=2,
                    avg_teaching=1, numratings=3, year=3, lecturer=l3, uni=gu, hits=453)

    c6 = add_course(code="CS3A", name="Advanced Programming 3", numratings=0, year=3, lecturer=l4, uni=gu)



    r3 = add_rating(c2, u1, datetime.now(), 4, 4 ,4, 4, 4, "Decent course, could be better")
    r7 = add_rating(c2, u3, datetime.now(), 4, 4 ,4, 4, 4)

    r5 = add_rating(c3, u5, datetime.now(), 9, 9 ,9, 9, 9)
    r6 = add_rating(c3, u4, datetime.now(), 9, 9 ,9, 9, 9)

    r9 = add_rating(c4, u6, datetime.now(), 3, 3 ,3, 3, 3)
    r11 = add_rating(c4, u4, datetime.now(), 3, 3 ,3, 3, 3)

    r13 = add_rating(c5, u6, datetime.now(), 1, 2 ,6, 2, 1)
    r14 = add_rating(c5, u1, datetime.now(), 1, 2 ,6, 2, 1)
    r8 = add_rating(c2, u4, datetime.now(), 4, 4 ,4, 4, 4, "This course was OK")
    r4 = add_rating(c3, u1, datetime.now(), 9, 9 ,9, 9, 9, "Average course.")

    r1 = add_rating(c1, u1, datetime.now(), 7, 5 ,3, 4, 10, "BAD COURSE - bloody terrible")
    r10 = add_rating(c4, u5, datetime.now(), 3, 3 ,3, 3, 3, "This course had much potential, but it was wasted at almost every opportunity.")
    r12 = add_rating(c5, u4, datetime.now(), 1, 2 ,6, 2, 1, "Average materials, difficulty etc but overall just terrible")

    r2 = add_rating(c1, u3, datetime.now(), 7, 5 ,3, 4, 10, "This is possibly the greatest course in the history of mankind")


def add_uni(name, email, country=None, city=None, tel=None) :
    u = University.objects.get_or_create(name=name, email_domain=email, country=country, city=city, telephone=tel)[0]
    return u

def add_user(username, email, password, can_add_course=False, first_name=None, last_name=None):
    u = User.objects.get_or_create(username=username, email=email, password=password, first_name=first_name or "", last_name=last_name or "")[0]
    u.set_password(u.password)
    u.save()
    if can_add_course:
        g = Group.objects.get_or_create(name="CourseAdders")[0]
        g.user_set.add(u)
    up = UserProfile()
    up.user = u
    up.save()
    return up

def add_lecturer(title, name, email=None, dept=None):
    l = Lecturer.objects.get_or_create(title=title, name=name,email=email, department=dept)[0]
    return l

def add_course(code, name, numratings, lecturer, uni, avg_overall=None, avg_difficulty=None, avg_teaching=None, avg_materials=None, avg_satisfaction=None, year=None, desc=None, hits=0):
    c = Course.objects.get_or_create(course_code=code, course_name=name, year_of_degree=year, description=desc, number_of_ratings=numratings, average_overall=avg_overall, average_difficulty=avg_difficulty,
                                     average_teaching=avg_teaching, average_materials=avg_materials, average_satisfaction=avg_satisfaction, lecturer=lecturer, uni=uni, hits=hits)[0]
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