from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    la=[]
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=5462ecc549d1ec03a3aa9f597e7075d0').read()
        json_data = json.loads(res)
        desc_string=str(json_data['weather'][0]['description']).upper()
        la.append(json_data['coord']['lon'])
        la.append(json_data['coord']['lat'])
        temp=round(json_data['main']['temp']-273.15,1)
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(json_data['coord']['lon']) + ' ' +
            str(json_data['coord']['lat']),
            "temp": temp,
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
            "desc":desc_string,
            "icon":str(json_data['weather'][0]['icon'])
        }

    else:
        city = ''
        data = {}
    return render(request, 'index.html', {'city': city, 'data': data,'la':la})