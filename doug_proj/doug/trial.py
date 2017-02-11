from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re

from credentials import CREDENTIALS
from peripherals import *

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

def post_facebook_message(fbid, data={}, message_text=None):
    if not message_text:
        user_details = get_user_details(fbid, ACCESS_TOKEN)
        message_text = 'Yo '+user_details.get('first_name', "")+'..! ' + data.get('recevied_message', "(no text")
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%ACCESS_TOKEN
    message_data = get_news_message_data("Sports", 5)


    response_data = {
        "recipient":{
            "id":fbid
        }, 
        "message": message_data
    }

    response_msg = json.dumps(response_data)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())




post_facebook_message(senderID, {"recevied_message": "original message"})

message_data = {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "generic",
            "elements": [{
                "title": "First card",
                "subtitle": "Element #1 of an hscroll",
                "image_url": "http://i1.kym-cdn.com/entries/icons/original/000/021/985/image.png",
                "buttons": [{
                    "type": "web_url",
                    "url": "https://www.messenger.com",
                    "title": "web url"
                }, {
                    "type": "postback",
                    "title": "Postback",
                    "payload": "Payload for first element in a generic bubble",
                }],
            }, {
                "title": "Second card",
                "subtitle": "Element #2 of an hscroll",
                "image_url": "https://img.clipartfest.com/a08f8728178012aca5a7d06e1801d2ae_-donald-trump-meme-image-trump-memes_800-623.jpeg",
                "buttons": [{
                    "type": "postback",
                    "title": "Postback",
                    "payload": "Payload for second element in a generic bubble",
                }],
            }]
        }
    }
}

