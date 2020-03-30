from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
import os
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
        weather_dict = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(weather_dict)
    print(weather_data)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)
