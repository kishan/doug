import json, requests, xmltodict

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


def summarize_article(url):
    headers = {'X-AYLIEN-TextAPI-Application-Key': 'f1ceba6c3a0b24ffd26d84c0a38168a1',
                'X-AYLIEN-TextAPI-Application-ID': 'b324016b'}
    params = {'url': url, 
              'sentences_number': 2}

    r = requests.get("https://api.aylien.com/api/v1/summarize", params=params, headers=headers)
    j = json.loads(r.text)

    try:
        return " ".join(j['sentences'])
    except Exception as e:
        return "Error summarizing article."

# summarize_article("https://www.washingtonpost.com/news/morning-mix/wp/2017/02/08/hillary-clinton-just-said-it-but-the-future-is-female-began-as-a-1970s-lesbian-separatist-slogan/?utm_term=.05294b4940db")
# parse_input("action: economy?", 1233333)


# input is a string of city
# returns list of dicts (events)
# each event has following variables: title, img, date, desc, url
def retrieve_local_events(city):
    ACCESS_TOKEN = "Z5FMtQdqjk34fLvP"
    params = {"app_key": ACCESS_TOKEN,
              "category": "politics_activism",
              "location": city}
    r = requests.get("http://api.eventful.com/rest/events/search?", params=params)
    xml = r.text
    j = json.loads(json.dumps(xmltodict.parse(xml)))
    # r = requests.get("http://api.eventful.com/rest/events/search?")
    events = []
    for event in j['search']['events']['event']:
        d = {}
        d['title'] = event["title"]
        d['date'] = event["start_time"]
        d['url'] = event["url"]
        try:
            d['img'] = event["image"]["medium"]["url"]
        except Exception as e:
            try:
                d['img'] = event["image"]["small"]["url"]
            except:
                d['img'] = "http://catholicinformation.org/wp-content/themes/fearless/images/missing-image-640x360.png"
        description = event["description"]
        if len(description) > 300:
            d['desc'] = description[:300] + "..."
        else:
            d['desc'] = description

        events.append(d)

    return events

retrieve_local_events("Pittsburgh")


