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
    todos = json.loads(response.text)
    articles = todos['articles']
    # print(type((articles)))
    counter = 0
    economistlist = []
    for art in articles:
        article = articles[counter]
        title = article['title']
        desc = article['description']
        link = article['url']
        content = article['content']
        altogether = title + "\n" + desc + "\n" + link + "\n" + content
        counter += 1
        economistlist.append(altogether)
    return economistlist
    



def send_message(text, chat_id):
    responsefromgetarticle = getarticle()
    for element in getarticle():
        titletext = urllib.parse.quote_plus(element)
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
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
