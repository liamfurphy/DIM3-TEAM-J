# RateMyCourse #

## Team J DIM3 Project ##


**To install:**

Install virtualenv and run "virtualenv env"
Activate your new virtualenv
run "pip install -r requirements.txt" to install project dependencies to your venv 

**To run:**

Make sure to activate your venv
first, sync the db by running "python manage.py syncdb"
say yes to create an admin account to be able to interact with the admin interface
after this is done, run "python populate_rmc.py" to populate the DB. NOTE this will throw RuntimeExceptions,
this is not an issue it is just cause by passing a python datetime object to Django (django still accepts the datetime from it though).
run "python manage.py runserver" to run the app on localhost port 8000

Test Accounts : Username: leifos Password: pass this account can rate courses and add new courses.

