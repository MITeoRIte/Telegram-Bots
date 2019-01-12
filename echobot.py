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
    from bs4 import BeautifulSoup
    import csv
    webpage = "https://www.economist.com/leaders/2018/12/22/the-world-is-fixated-on-the-past"
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, 'html.parser')
    name_box = soup.find(class_='blog-post main-content__blog-post main-content__main-column blog-post--template-article')
    #CONTENT
    onlyp = name_box.find_all('p')
    story1 = ""
    story2 = ""
    lengthofonlyp = int(len(onlyp))
    print("Length of onlyp is " + str(lengthofonlyp))
    counter = 0

    for element in onlyp:
        print("in loop for " + str(element) + " times")
        counter += 1
        if counter >= lengthofonlyp/2:
            print(str(element) + " appended to story2")
            story2 += str(element.contents[0])
        else:
            print(str(element) + " appended to story1")
            story1 += str(element.contents[0])
            
    print("stories set.")

    #TITLE
    title = soup.find(class_='flytitle-and-title__title')
    gettitle = title.contents[0].upper()
    #ALTOGETHER
    altogether = [gettitle, story1.strip('span'), story2.strip('span')]
    return altogether



def send_message(text, chat_id):
    for element in getarticle():
        titletext = urllib.parse.quote_plus(str(element))
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
