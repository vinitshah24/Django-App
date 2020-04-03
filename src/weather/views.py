from django.shortcuts import render, redirect
from dotenv import load_dotenv
import requests
import json
import os

from .models import City
from .forms import CityForm

env_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '.env')
)
load_dotenv(env_file)


def index(request):
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + \
        os.environ.get('WEATHER_APP_KEY')

    error_msg = ''
    message = ''
    alert = ''

    # Saves form data directly to the table
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name'].title()
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(weather_url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'Invalid City Name!'
            else:
                error_msg = 'City Already Added!'

    if error_msg == 'Invalid City Name!':
        message = error_msg
        alert = 'alert-danger'
    elif error_msg == 'City Already Added!':
        message = 'City Added Successfully'
        alert = 'alert-success'

    form = CityForm()
    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(weather_url.format(city)).json()
        weather_dict = {
            'city': city.name.title(),
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'description': r['weather'][0]['description'].title(),
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(weather_dict)
    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'alert': alert,
    }
    return render(request, 'index.html', context)


def delete_city(request, city):
    City.objects.get(name=city.lower()).delete()
    return redirect('home')
