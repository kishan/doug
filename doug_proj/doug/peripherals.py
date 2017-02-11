import requests, json

########### News Grab Retrieve Top 5 #############

# input: n: number of articles to retreive
# returns: json of top n political news articles
def retrieve_news(category, n):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '42c55ca1b83d47e7b0b21f70f06d9087',
    }
    params = {
        # Request parameters
        'Category': category,
    }

    try:
        r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/?', params=params, headers=headers)
        j = json.loads(r.text)

        for i in range(n):
            print (j['value'][i]['name'])
            print (j['value'][i]['url'])
            print ("--------------------")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))




################# Retrieve Charities #####################

def retrieve_charities(query):

    params = {
        'user_key': 'a77675d1a89b044899df9397133d29c4',
        'searchTerm': query,
    }
    r = requests.post("http://data.orghunter.com/v1/charitysearch", params=params)
    j = json.loads(r.text)
    for article in j['data']:
        print (article['charityName'])
        print (article['url'])
        print ("\n")  


retrieve_news('Health', 20)



