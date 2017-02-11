from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import re
from messengerbot import MessengerClient, messages, attachments, templates, elements
from doug.credentials import CREDENTIALS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from doug.classifier import *
from doug.peripherals import *
from doug.intent_parsing import *

ACCESS_TOKEN = CREDENTIALS['ACCESS_TOKEN']
VALIDATION_TOKEN = CREDENTIALS['VALIDATION_TOKEN']
API_KEY = CREDENTIALS['API_KEY']
messenger = MessengerClient(access_token=ACCESS_TOKEN)

def index(request):
    article_url = request.GET('article_url')
    category = classify(article_url)
    return HttpResponse(category)

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
        phone = senator_info['phones'][0]
        phone = re.sub('\s', '', phone)
        phone = re.sub('[!@#$()-]', '', phone)
        senator = {'name': senator_info['name'], 'phone': phone}
        senators.append(senator)
    return senators

def get_user_details(fbid, access_token_val):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':access_token_val}
    user_details = requests.get(user_details_url, user_details_params).json()
    return user_details



def post_facebook_message(fbid, data={}, send_ready=False):
    try:

        message_data = None
        if send_ready == True:
            message_data = data


        recevied_message = str.lower(data.get('recevied_message', ""))

        if (recevied_message) and ('news' in recevied_message):
            print("GETTING NEWS")
            message_data = get_news_message_data(recevied_message)


        if message_data is None:
            user_details = get_user_details(fbid, ACCESS_TOKEN)
            message_text = 'Yo '+user_details.get('first_name', "")+'..! ' + data.get('recevied_message', "(no text")
            # message_data = {"text":"If I die all I know is I'm a Mothafuckin legend"}
            message_data = {"text":message_text}


        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%ACCESS_TOKEN

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
            # print("senderID: " + str(senderID))
            message_obj = i['message']
            if 'text' in message_obj:
                recevied_message = message_obj["text"]
                # TODO: check if first time user
                # if not senderID in chat.conversation:
                    #Initiate user info
                    # initiateChat(senderID)
                post_facebook_message(senderID, {"recevied_message": recevied_message})
            elif 'attachments' in message_obj:
                post_facebook_message(senderID, {text:"Don't know how to handle attachments"}, send_ready=True)
        elif "postback" in i:
            # print(i)
            payload = i.get('postback', {}).get('payload', "")
            # print("payload = " + payload)
            senderID = i["sender"]['id']
            handle_payload(senderID, payload)
    return HttpResponse("It's working")


def handle_payload(fbid, payload):
    if "SUMMARIZE_PAYLOAD" in payload:
        # payload_val should be url to article
        payload_val = payload.split(':', 1)[1]
        article_summary = summarize_article(payload_val)
        post_facebook_message(fbid, data={'text':article_summary}, send_ready=True)
    if "TAKE_ACTION_PAYLOAD" in payload:
        # payload should be url to article
        payload_val = payload.split(':', 1)[1]
        action_handeling(fbid)
        # post_facebook_message(fbid, data={'text':payload_val}, send_ready=True)
    if "CONTACT_REP_PAYLOAD" in payload:
        post_facebook_message(fbid, data={'text':"Contact Your Local Rep!!!"}, send_ready=True)
        contact_rep_handeling(fbid)
    if "DONATE_NO_CAT_PAYLOAD" in payload:
        post_facebook_message(fbid, data={'text':"DONATE!!! (no cat)"}, send_ready=True)
    if "DONATE_PAYLOAD" in payload:
        post_facebook_message(fbid, data={'text':"DONATE!!!"}, send_ready=True)
    if "LOCAL_EVENTS_PAYLOAD" in payload:
        post_facebook_message(fbid, data={'text':"Discover Local Events!!!"}, send_ready=True)

def contact_rep_handeling(fbid, location="Pittsburgh, PA"):
    senator_info = senators_phone(location)
    # post_facebook_message(fbid, data={'text':str(senator_info)}, send_ready=True)

    buttons = []
    for senator in senator_info:
        # {'name': 'Robert P. Casey Jr.', 'phone': '(202) 224-6324'}
        button = {
          "type":"phone_number",
          "title": "Call " + str(senator['name']),
          "payload": senator['phone']
          # "payload":"3476988212"
       }

        buttons.append(button)

    message_data = {
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":"Here are your local representatives you can contact!!!",
            "buttons": buttons
          }
        }
    }

    # post_facebook_message(fbid, data={'text':str(buttons)}, send_ready=True)
    print(message_data)
    post_facebook_message(fbid, data=message_data, send_ready=True)






def action_handeling(fbid, article_cat=None):
    message_data = {
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":"How would you like to take action?",
            "buttons":[
              {
                "type":"postback",
                "title":"Contact a Rep",
                "payload":"CONTACT_REP_PAYLOAD"
              }, {
                "type":"postback",
                "title":"Donate to a Cause",
                "payload": "DONATE_PAYLOAD:" + str(article_cat) if article_cat else "DONATE_NO_CAT_PAYLOAD:"
              }, {
                "type":"postback",
                "title":"Discover Local Events",
                "payload":"LOCAL_EVENTS_PAYLOAD"
              }
            ]
          }
        }
    }

    post_facebook_message(fbid, data=message_data, send_ready=True)


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
