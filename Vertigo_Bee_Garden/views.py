import requests
from django.shortcuts import render

def home(request):
    city = "Karczewiska"
    lat = 51.24
    lon = 16.12
    api_key = "e0e9095f907ebd7a5f441366e045ffa7"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"


    weather = {}
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            weather = {
                'city': city,
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else:
            weather['error'] = data.get('message', 'Błąd pobierania pogody.')
    except Exception:
        weather['error'] = 'Błąd połączenia.'

    return render(request, "base.html", {'weather': weather})