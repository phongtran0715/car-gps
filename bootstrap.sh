#!/bin/bash
echo 'Creating virtualenv...'
python3 -m venv venv

echo 'Installing requirement packages...'
source $PWD/venv/bin/activate
python3 -m pip install -r requirements.txt

echo 'Init database'
python3 manage.py makemigrations
python3 manage.py migrate

echo 'Project initialization is complete!'
echo 'Start the project:'
python3 manage.py runserver 8000