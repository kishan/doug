from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from messengerbot import MessengerClient, messages, attachments, templates, elements
from doug.credentials import CREDENTIALS
from doug.peripherals import *



ACCESS_TOKEN = CREDENTIALS['ACCESS_TOKEN']
VALIDATION_TOKEN = CREDENTIALS['VALIDATION_TOKEN']
API_KEY = CREDENTIALS['API_KEY']
messenger = MessengerClient(access_token=ACCESS_TOKEN)



def index(request):
    return HttpResponse("Hi, my name is Doug.")

def senators_phone(address):
    payload = {
        'key': 'AIzaSyBXie2DAg6CPE6YOfikEDi_Io_LBDD1h9M',
        'address': address, 
        'roles': 'legislatorUpperBody'
    }
    req_url = 'https://www.googleapis.com/civicinfo/v2/representatives'
    res = requests.get(req_url, params=payload).json()
    senators_info = res['officials']
    senators = []
    for senator_info in senators_info:
        senator = {'name': senator_info['name'], 'phone': senator_info['phones'][0]}
        senators.append(senator)
    return HttpResponse(senators)


def get_user_details(fbid, access_token_val):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':access_token_val} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    return user_details

def post_facebook_message(fbid, data={}, message_text=None):
    try:
        if not message_text:
            user_details = get_user_details(fbid, ACCESS_TOKEN)
            message_text = 'Yo '+user_details.get('first_name', "")+'..! ' + data.get('recevied_message', "(no text")
                       
        if ('recevied_message' in data):
            recevied_message = str.lower(data['recevied_message'])
        else:
            recevied_message = None

        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%ACCESS_TOKEN
        message_data = {"text":message_text}
        
        if (recevied_message) and ('news' in recevied_message):
            message_data = get_news_message_data()

        response_data = {
            "recipient":{
                "id":fbid
            }, 
            "message": message_data
        }

        response_msg = json.dumps(response_data)
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        # print(status.json())
    except Exception as e:
        try:
            print(e)
        except:
            print("DONT KNOW WTF THE ERROR IS")



def chathandler(request):
    print("HANDELING MESSAGE")
    body = request.body.decode('utf-8')
    if body:
        data = json.loads(request.body.decode('utf-8'))
    else:
        data = {}
    # print(data)
    for i in data["entry"][0]["messaging"]:
        if "message" in i:
            print("MESSAGE!!!")
            senderID = i["sender"]['id']
            # senderID = '1339285402812293'
            print("senderID: " + str(senderID))
            message_obj = i['message']
            if 'text' in message_obj:
                recevied_message = message_obj["text"]
                print('recevied_message: ' + str(recevied_message)) 
                # TODO: check if first time user
                # if not senderID in chat.conversation:
                    #Initiate user info
                    # initiateChat(senderID)
                post_facebook_message(senderID, {"recevied_message": recevied_message})
            elif 'attachments' in message_obj:
                post_facebook_message(senderID, {}, "Don't know how to handle attachments")
        elif "postback" in i:
            payload = i.get('postback', {}).get('payload', "")
            # print("payload = " + payload)
            handle_payload(payload)
    return HttpResponse("It's working")

def handle_payload(payload):
    if "ARTICLE_PAYLOAD" in payload:
        payload_val = payload.split(':', 1)[1]


@csrf_exempt
def webhook(request):
    print("________________________________________________________________________")
    print("REQUEST RECEIVED")
    if request.method!="POST":
        #Validate URL
        print("Validating Verify Token")
        if request.GET.get('hub.verify_token', "") == VALIDATION_TOKEN:
            return HttpResponse(request.GET['hub.challenge'])
        return HttpResponse("Failed validation. Make sure the validation tokens match.")
    return chathandler(request)

