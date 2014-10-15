Tutoring-Center-Calendar
========================

A web application that allows students to make appointments with tutors in the CCI tutoring center.

Warning--at the moment, you need Django 1.6.5. This project breaks with Django 1.7!

###Requirements
*   Django 1.6.5
*   Python 2.7


###Installation
1. Install [Django 1.6.5](https://www.djangoproject.com/)
2. Install [Django-Bootstrap-3](https://github.com/dyve/django-bootstrap3)
3. Install [Django-Bootstrap-Calendar](https://github.com/sandlbn/django-bootstrap-calendar) (i.e., run `python setup.py install`)
4. Install [jsmin 2.0.9](https://pypi.python.org/pypi/jsmin)

###How to Run
1. `cd` into the "Tutoring-Application" folder
2. Enter `python manage.py syncdb` into the terminal. Follow the instructions if it's the first time running that command (if so, there won't be a db.sqlite file). You only need to do this once.
3. Enter `python manage.py runserver` into the terminal.
4. Point your browser to http://localhost:8000


###FAQ
1. How do I remove all database entries / reset the application?
Remove the sqlite file to remove all database entries of the application (however, you will need to run `python manage.py syncdb` again).
2. Do I need to run `python manage.py syncdb` everytime I run the application?
No, you only need to run that command once. Once the database is synced, just run `python manage.py runserver` thereafter to run the application.
