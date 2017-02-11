from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from messengerbot import MessengerClient, messages, attachments, templates, elements
from doug.credentials import CREDENTIALS


ACCESS_TOKEN = CREDENTIALS['ACCESS_TOKEN']
VALIDATION_TOKEN = CREDENTIALS['VALIDATION_TOKEN']
API_KEY = CREDENTIALS['API_KEY']
messenger = MessengerClient(access_token=ACCESS_TOKEN)



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def senators_phone(request, address):
    pass

@csrf_exempt
def test(request):
	hub_token = request.GET.get('hub.challenge', 'nothing found')
	print("API HIT")
	body = request.body.decode('utf-8')
	if body:
		incoming_message = json.loads(request.body.decode('utf-8'))
	else:
		incoming_message = {}
	print(incoming_message)
	print("**********")

	method = request.method
	if method == "GET":
		print("GET REQUEST")
		print(request.GET)
	if method == "POST":
		print("POST REQUEST")
		print(request.POST)
	return HttpResponse(hub_token)



def respondToClient(senderID, received_message):
    recipient = messages.Recipient(recipient_id=senderID)
    text_to_respond = "WOrking now?!!!"

    response = messages.MessageRequest(recipient, messages.Message(text=text_to_respond))
    #send message to Messenger
    messenger.send(response)


def chathandler(request):
    print("HANDELING MESSAGE")
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    for i in data["entry"][0]["messaging"]:
        if "message" in i:
            print("MESSAGE!!k!")
            senderID = i["sender"]['id']
            # senderID = '1339285402812293'
            print("senderID: " + str(senderID))
            print('i["message"]["text"] :' + str(i["message"]["text"])) 
            # if not senderID in chat.conversation:
                #Initiate user info
                # initiateChat(senderID)
            respondToClient(senderID,i["message"]["text"])
    return HttpResponse("It's working")

@csrf_exempt
def webhook(request):
    print("REQUEST RECEIVED")
    if request.method!="POST":
        #Validate URL
        print("Validating Verify Token")
        if request.GET['hub.verify_token'] == VALIDATION_TOKEN:
            return HttpResponse(request.GET['hub.challenge'])
        return HttpResponse("Failed validation. Make sure the validation tokens match.")
    return chathandler(request)








