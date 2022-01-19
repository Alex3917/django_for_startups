# django_for_startups
Code for the book [Django for Startups](https://alexkrupp.typepad.com/sensemaking/2021/06/django-for-startup-founders-a-better-software-architecture-for-saas-startups-and-consumer-apps.html)

## Instructions for running locally on MacOS with Python 3.8:

1. Create a virtualenv using `python3 -m venv .`

2. Activate the virtualenv with `. bin/activate`

3. Install pip-tools using: `pip install pip-tools`

4. Run `pip-compile --output-file requirements.txt requirements.in && pip install -r requirements.txt`. This generates the requirements.txt file from the requirements.in file. If this doesn't work, try upgrading setuptools.

5. If not already installed, install Homebrew: https://brew.sh/.

6. Run `brew update`

7. Install Redis locally on your mac: `brew install redis`

8. Start redis locally using: `brew services start redis`

## Start server:
python django_for_startups/manage.py runserver

## Run tests:
python django_for_startups/manage.py test

## Check for outdated root dependencies:
python scripts/list_outdated.py
