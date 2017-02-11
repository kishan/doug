import requests, json

########### News Grab Retrieve Top 5 #############

# input: n: number of articles to retreive
# returns: json of top n political news articles
def retrieve_news(category="Politics", n=5):

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
        data = json.loads(r.text)
        list_news = data.get('value', [])

        final = []
        articles_num = min(len(list_news), n)
        for i in range(articles_num):
            title = list_news[i].get('name', "(no title)")
            url = list_news[i].get('url', "")
            thumbnail = list_news[i].get('image', {}).get('thumbnail', {}).get('contentUrl', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAAYFBMVEXa2tpVVVXd3d1MTExSUlK2trZvb29LS0tTU1Ph4eGNjY2cnJzU1NRaWlpgYGBPT0+np6fGxsavr6/AwMCGhoaioqJpaWnMzMx+fn6UlJS7u7t1dXWzs7NERERkZGSdnZ1LtC8/AAACkElEQVR4nO3b626qQBRAYeYiM2NVVPCCWvv+b3lEUUDhpIpJ42Z9/0qFOCsTYFCjCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwCPqN/nosr9Grdfw+4a+H8xL95bx9F/+pDRL1PjSgAQ0kNLDOuFeZxHgBDZJ8N+phNxPQwCxDn3ujMPMCGsx7vX0hDXrd54pokDzZ4G5pMLwGWqfL5aa+w+Aa6EV8upDarLZpaA30wtvzKWRfbRtcg315Z+mqfYbWYHO9ufbxUBvokbmuDqaiG/wvSHprMJPcQI+2nRV0VK4NVJLdhiyxwdqNO4ej59+X04HfCJ4HemmUybsj5C7xiVG76hXyGkTH04jMT3eENIvjfBOqXcQ10KvzWc+tuiPoEEJ9ySCuQTS9DKh4ptB4afdRpDUIeVI+GXOH+pj0rjuCtAaT6+VfeVsf9kRtO6eCsAYhqz1odmk1PbIkWU86IshqoDemSqDsdHHb7k5/HjftEYQ12DY+b7C2HHXYFwtmm6StwxTVQKdONdjZOYI+XKaH9cu2cYpqEGKr7iNMin+Ug+y4bZDUoLYwvinOhPqr2m7Gj+cESQ2itX9ooGwcTWqbvXm8RgpqEOatH8Am26yx/TwzGkcR1ECrlmlQzIS7NHa2kNogrB7PBu1sfeEcSWowmf4yQbFD4xoppoFe/HYaFFweqlOjoAZPfSXFZAKfoTzZQJn9bQklqUH7ZaGDN6clVHl7KaeBnz4rvRxFTIPTheF5l6MIavAyGohpEHo5Cmjg9+M+8vIO86MbnJZFvSgJDd6DBjSgwUc3yL/NuzjzmQ2ixaHPl/abDh/64z5+3wgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAz/kH0Z07XHC7XZ8AAAAASUVORK5CYII=')
            description = list_news[i].get('description', "")
            article_data = {
                'title': title,
                'url': url,
                'thumbnail': thumbnail,
                'description': description
            }
            final.append(article_data)


            # print(name)
            # print(url)
            # print(thumbnail)
            # print(description)
            # print("--------------------")
        return final
    except Exception as e:
        try:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return []
        except:
            print("DONT KNOW WTF THE ERROR IS")
            return []

def query_news(query, n=5):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '42c55ca1b83d47e7b0b21f70f06d9087',
    }
    params = {
        # Request parameters
        'q': query,
    }

    try:
        r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/news/search?', params=params, headers=headers)
        data = json.loads(r.text)
        list_news = data.get('value', [])

        final = []
        articles_num = min(len(list_news), n)
        for i in range(articles_num):
            title = list_news[i].get('name', "(no title)")
            url = list_news[i].get('url', "")
            thumbnail = list_news[i].get('image', {}).get('thumbnail', {}).get('contentUrl', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAAYFBMVEXa2tpVVVXd3d1MTExSUlK2trZvb29LS0tTU1Ph4eGNjY2cnJzU1NRaWlpgYGBPT0+np6fGxsavr6/AwMCGhoaioqJpaWnMzMx+fn6UlJS7u7t1dXWzs7NERERkZGSdnZ1LtC8/AAACkElEQVR4nO3b626qQBRAYeYiM2NVVPCCWvv+b3lEUUDhpIpJ42Z9/0qFOCsTYFCjCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwCPqN/nosr9Grdfw+4a+H8xL95bx9F/+pDRL1PjSgAQ0kNLDOuFeZxHgBDZJ8N+phNxPQwCxDn3ujMPMCGsx7vX0hDXrd54pokDzZ4G5pMLwGWqfL5aa+w+Aa6EV8upDarLZpaA30wtvzKWRfbRtcg315Z+mqfYbWYHO9ufbxUBvokbmuDqaiG/wvSHprMJPcQI+2nRV0VK4NVJLdhiyxwdqNO4ej59+X04HfCJ4HemmUybsj5C7xiVG76hXyGkTH04jMT3eENIvjfBOqXcQ10KvzWc+tuiPoEEJ9ySCuQTS9DKh4ptB4afdRpDUIeVI+GXOH+pj0rjuCtAaT6+VfeVsf9kRtO6eCsAYhqz1odmk1PbIkWU86IshqoDemSqDsdHHb7k5/HjftEYQ12DY+b7C2HHXYFwtmm6StwxTVQKdONdjZOYI+XKaH9cu2cYpqEGKr7iNMin+Ug+y4bZDUoLYwvinOhPqr2m7Gj+cESQ2itX9ooGwcTWqbvXm8RgpqEOatH8Am26yx/TwzGkcR1ECrlmlQzIS7NHa2kNogrB7PBu1sfeEcSWowmf4yQbFD4xoppoFe/HYaFFweqlOjoAZPfSXFZAKfoTzZQJn9bQklqUH7ZaGDN6clVHl7KaeBnz4rvRxFTIPTheF5l6MIavAyGohpEHo5Cmjg9+M+8vIO86MbnJZFvSgJDd6DBjSgwUc3yL/NuzjzmQ2ixaHPl/abDh/64z5+3wgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAz/kH0Z07XHC7XZ8AAAAASUVORK5CYII=')
            description = list_news[i].get('description', "")
            article_data = {
                'title': title,
                'url': url,
                'thumbnail': thumbnail,
                'description': description
            }
            final.append(article_data)


            # print(name)
            # print(url)
            # print(thumbnail)
            # print(description)
            # print("--------------------")
        card_elements = list(map(format_news_to_card, final))
        print(card_elements)

        if card_elements == []:
            return {"text": "No news found regarding that subject"}
        message_data = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": card_elements
                }
            }
        }
        return message_data
    except Exception as e:
        try:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return []
        except:
            print("DONT KNOW WTF THE ERROR IS")
            return []




def get_news_message_data(subject="Politics", n=5):
    # news_data = retrieve_news(subject, n)
    news_data = query_news("politics " + subject, n)
    card_elements = list(map(format_news_to_card, news_data))
    print(card_elements)

    if card_elements == []:
        return {"text": "No news found regarding that subject"}
    message_data = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": card_elements
            }
        }
    }
    return message_data

def format_news_to_card(news):
    card = {
        "title": news['title'],
        "subtitle": news['description'],
        "image_url": news['thumbnail'],
        "buttons": [{
            "type": "web_url",
            "url": news['url'],
            "title": "View on Web"
        }, {
            "type": "postback",
            "title": "Summarize",
            # "payload": "SUMMARIZE_PAYLOAD:" + str(news['url']),
            "payload": "SUMMARIZE_PAYLOAD:" + str(news['url']),
        }, {
            "type": "postback",
            "title": "Take Action",
            "payload": "TAKE_ACTION_PAYLOAD:" + str(news['url']),
        }],
    }
    return card

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


retrieve_news('Health', 5)



