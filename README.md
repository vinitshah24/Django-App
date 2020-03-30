# Django Weather App

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

Create virtual environment for the application:<br />
```
virtualenv .
```
 
Source scripts to activate the virtualenv:<br />
```
source Scripts/activate
```
 
Install requirements for the project:<br />
```
pip install -r requirements.txt
```
 
Navigate to src/ directory and run the following commands:<br />
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```