import json, requests

def parse_input(input, sessionId):
    ACCESS_TOKEN = "98e6888bd8c34796aed02fd9f35b5b5c"

    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    params = {'query': input,
              'sessionId': sessionId,
              'lang': "en"}

    r = requests.get("https://api.api.ai/v1/query", params=params, headers=headers)
    j = json.loads(r.text)

    print(j)
    try:
        bot_response = j['result']['speech']
    except Exception as e:
        bot_response = None

    try:
        bot_parameters = j['result']['parameters']["Subjects"]
    except Exception as e:
        bot_parameters = None

    bot_intent = j['result']['metadata']['intentName']

    print ("intent: " + bot_intent)
    if bot_parameters:
        print ("topic is: "+ bot_parameters)
    if bot_response:
        print ("bot says: "+ bot_response)



parse_input("action: economy?", 1233333)
