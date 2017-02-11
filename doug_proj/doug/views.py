from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    return HttpResponse("Hi, my name is Doug.")

def senators_phone(address):
    payload = {'key': 'AIzaSyBXie2DAg6CPE6YOfikEDi_Io_LBDD1h9M',
        'address': address, 'roles': 'legislatorUpperBody'}
    req_url = 'https://www.googleapis.com/civicinfo/v2/representatives'
    res = requests.get(req_url, params=payload).json()
    senators_info = res['officials']
    senators = []
    for senator_info in senators_info:
        senator = {'name': senator_info['name'], 'phone': senator_info['phones'][0]}
        senators.append(senator)
    return HttpResponse(senators)
