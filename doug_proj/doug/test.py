from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from messengerbot import MessengerClient, messages, attachments, templates, elements
import re

access_token = 'EAAR5DG8bSxwBAHY6xEl9WhOxNHkyog6NqM727oUCly4Vh7A8ZC2AzOd1D4hEVIN40hiAqOy02sgJZCR1YMcZCjPoR7R9IriNhrxAhxmsHvCmkrn5JhXSInq0gXrKNj4LZAKIJ5AqmR5g9EpECMaVZBHvoH5dJqa1YImlUjtwnogZDZD'
VALIDATION_TOKEN= '22504'
api_key = '< API key >'
messenger = MessengerClient(access_token=access_token)

senderID = '1418505298170751'
recipientID = '1339285402812293'
senderID = recipientID

message = "TRIAL FOR YOU"
data = {'object': 'page', 'entry': [{'id': '1418505298170751', 'time': 1486790071855, 'messaging': [{'sender': {'id': '1418505298170751'}, 'recipient': {'id': '1339285402812293'}, 'timestamp': 1486789719456, 'message': {'is_echo': True, 'app_id': 1258994217470748, 'mid': 'mid.1486789719456:573f948f31', 'seq': 459157, 'text': 'I WANT POPCORN!!!'}}]}]}
recipient = messages.Recipient(recipient_id=senderID)
result = "sadfsdf HEYOO!!!"
response = messages.MessageRequest(recipient, messages.Message(text=result))
messenger.send(response)



def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    joke_text = "KNOCK KNOCK"

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':access_token} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    print(user_details)
    joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%access_token
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # pprint(status.json())




post_facebook_message(senderID, "original message")


