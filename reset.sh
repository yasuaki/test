#!/bin/sh

git checkout -- dev.db
python manage.py syncdb
#python manage.py dumpdata --indent=2 si > dump/si/initial_data.json
python manage.py runserver
