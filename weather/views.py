from datetime import datetime, tzinfo
from time import timezone
from django.shortcuts import render
import json
import urllib.request
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib.request
import requests
# Create your views here.


def index(request):
    #Showing Weather Report And Map Location
    la=[]
    if request.method == 'POST' and "city":
        global city 
        city= request.POST['city']
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
        # geores=urllib.request.urlopen('https://api.hostip.info/get_json.php').read()
        # geores=json.loads(geores)
        # print(geores)
        return render(request, 'index.html', {'city': city, 'data': data,'la':la})

    
    else:
        city = ''
        data = {}
        la=[]
        return render(request, 'index.html', {'city': city, 'data': data,'la':la})

####################################################
   
## if you don't want to user rest_framework
   
# def get_data(request, *args, **kwargs):
#
# data ={
#             "sales" : 100,
#             "person": 10000,
#     }
#
# return JsonResponse(data) # http response
   
   
#######################################################


## using rest_framework classes
   
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format = None):
        datavres=urllib.request.urlopen('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+city+'?unitGroup=metric&key=U8XMTFZLWN2Y59MYJMERZGT6U&include=fcst%2Cstats%2Calerts%2Ccurrent').read()
        datav_json_data=json.loads(datavres)
        date=[]
        temperature=[]
        pressure=[]
        for i in range(15):
            date.append(str(datav_json_data['days'][i]['datetime']))
            temperature.append(datav_json_data['days'][i]['temp'])
            pressure.append(datav_json_data['days'][i]['pressure'])
        chartLabel = "my data"
        chartdata = []
        labels=[]
        labels=date
        desc=datav_json_data['description']
        chartdata=temperature
        pressure_chardata=pressure
        data ={
                     "labels":labels,
                     "chartLabel":chartLabel,
                     "chartdata":chartdata,
                     "pressureData":pressure_chardata,
                     'desc':desc,
             }
        return Response(data)
