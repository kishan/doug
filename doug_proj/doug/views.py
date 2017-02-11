from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def senators_phone(request, address):
    pass
