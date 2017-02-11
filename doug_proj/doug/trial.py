from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re

from credentials import CREDENTIALS

ACCESS_TOKEN = CREDENTIALS['ACCESS_TOKEN']
VALIDATION_TOKEN = CREDENTIALS['VALIDATION_TOKEN']
API_KEY = CREDENTIALS['API_KEY']


senderID = '1418505298170751'
recipientID = '1339285402812293'
senderID = recipientID

def get_user_details(fbid, access_token_val):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':access_token_val} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    return user_details

def post_facebook_message(fbid, recevied_message):
    user_details = get_user_details(fbid, ACCESS_TOKEN):    
    message_text = "I'M ALIVE!!!"
    message_text = 'Yo '+user_details.get('first_name', "")+'..! ' + message_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%ACCESS_TOKEN
    response_data = {
        "recipient":{
            "id":fbid
        }, 
        "message":{
            "text":message_text
        }
    }
    response_msg = json.dumps(response_data)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())


post_facebook_message(senderID, "original message")


