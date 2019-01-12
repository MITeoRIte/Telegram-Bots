import json
import requests
import time
import urllib


TOKEN = "640526598:AAExQPhjGeDI2FdMhhS579-GTqZbY_HVZpQ"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def getarticle():

# #Webscraper learning

    import requests
    import json


    response = requests.get("https://newsapi.org/v2/top-headlines?sources=the-economist&apiKey=73756f6d2dc6451399fcb0b15ad9d8cc")
    nyt = requests.get("https://newsapi.org/v2/top-headlines?sources=the-new-york-times&apiKey=73756f6d2dc6451399fcb0b15ad9d8cc")
    todos = json.loads(response.text)
    nyttodos = json.loads(nyt.text)
    articles = todos['articles']
    nytarticles = nyttodos['articles']
    # print(type((articles)))
    economistlist = []
    nytlist = []
    for i in range(0,3):
        article = articles[i]
        title = article['title']
        desc = article['description']
        link = article['url']
        content = article['content']
        altogether = title + " " + link + " "
        economistlist.append(altogether)
    for i in range(0, len(nytarticles)-1):
        article = nytarticles[i]
        title = article['title']
        desc = article['description']
        link = article['url']
        content = article['content']
        altogether = title + " " + link + " "
        nytlist.append(altogether)
        print(altogether)
    return economistlist
    
from datetime import date



def send_message(text, chat_id):
    titletext = urllib.parse.quote_plus("Here are the top 3 articles from The Economist for " + str(date.today()))
    url = URL + "sendMessage?text={}&chat_id={}".format(titletext, chat_id)
    get_url(url)
    # for element in getarticle():
    for article in getarticle():
        tosend = article.strip('[')
        tosend = tosend.strip(']')
        titletext = urllib.parse.quote_plus(tosend)
        url = URL + "sendMessage?text={}&chat_id={}".format(titletext, chat_id)
        get_url(url)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
        print("getting updates")

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def echo_all(updates):
    
    for update in updates["result"]:
        print(update["message"]["text"])
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
