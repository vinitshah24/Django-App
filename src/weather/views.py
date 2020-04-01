from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
import os
import json
# Create your views here.


def index(request):
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + \
        os.getenv('WEATHER_APP_KEY')

    # Saves form data directly to the table
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(weather_url.format(city)).json()
        with open('test.json', 'w+', encoding='utf-8') as json_file:
            json.dump(r, json_file, ensure_ascii=False, indent=2)
        weather_dict = {
            'city': city.name.title(),
            'temperature': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'description': r['weather'][0]['description'].title(),
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(weather_dict)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)
