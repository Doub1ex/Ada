#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import random
import re
import time
import requests
from multiprocessing import Process
from urllib.parse import urlencode
from googleapiclient.discovery import build


# from Ada import *
# import argparse
# from urllib import request
# from moviepy.editor import *



from config import *
from DictData import *

head = {'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:39.0) Gecko/39.0 Firfox/39.0',
        'Language': 'en-US,en;q=0.5 | en-US',
        'Accept': 'text/html,application/xhtml + xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate'}
headm = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
         'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded',
         'Referer': 'http://google.com/'}


morningtime = " 09:00:00 "

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#t9typelist = {"гиф": "mp4", "каритин": "jpg"}
#t9catlist = ["cosplay", "wtf", "girl", "meme", "geeky", "comic", "food", "cute"]


modes = {"youtube": 2, "ютуб": 2, "музы": 1}
resourses = {"пикабу": "pikabu", "вики": "wiki", "wiki": "wiki", "интерес": "wiki", "баш": "bashorg", "9gag": "t9gag"}


chatlist = {'someabstractchat': 1}
userlist = {'someabstractuser': 1}


memory = {"user0": [""]}

name = ""

# mood = 499
# def normalizemood():
#    mood+=int(mood-499)

def keepinmemory(message, user):
    try:
        mem = memory[user]
        if len(mem) > 3:
            mem.pop(0)
        mem.append(message.strip())
        memory.update({user: mem})
        print(mem, "saved")
    except Exception as e:
        memory.update({user: [message]})
        print(str(e))
        print(message, "created")
    return


def callfrommemory(user):
    try:
        mem = memory[user]
    except:
        mem = [""]
    return mem


def myunitime(imputime):
    return int(time.mktime(time.strptime(imputime, '%Y-%m-%d %H:%M:%S')))


def randList(listForRand):
    random.shuffle(listForRand)
    return listForRand[0]


def opentheurl(baseurl, method, params):
    r = requests.get(str(baseurl + method + urlencode(params)), headers=head, timeout=3)
    return r.text


def dickify(message):
    cn = 0
    message = message.split(' ')[-1]
    for i in message:
        cn += 1
        for x in xylist.keys():
            if x == i:
                return xylist[x] + message[-(len(message) - cn - len(xylist[x]) + 3):], ""
    return "", ""


def accost(message):
    message = message.replace("\'", "\"")
    st = ''
    if "\"" in message:
        st = message.split("\"")[1]
        while st in message:
            st = message.split("\"")[1]
            message = message.replace("\"" + st + "\"", "")
            if st in message:
                message = message.replace("\"" + st, "")
    message = "".join(re.compile("[\"\'a-zA-Zа-яА-Я0-9 -]").findall(message))
    message = message.replace("  ", " ").replace("-", " ")
    words = message.lower().replace("a", "а").replace("d", "д").replace("o", "о").replace("y", "у").replace("e",
                                                                                                            "е").split(
        " ")
    for word in words:
        i = 0
        while i < len(word) - 1:
            if (word[i] == word[i + 1]):
                word = word[:i] + word[i + 1:]
            else:
                i += 1
        if len(word) >= 2:
            st = str(word[:2])
            if (st == 'ад') and (len(word) == 2):
                return word
            if (st == 'ад') and ((word[2] in gl) or (len(word) == 3 and word[2] == "а")):
                return word
    return ""


def rname(message, name):
    messtmp = message.replace("\'", "\"")
    st = ''
    if "\"" in messtmp:
        st = messtmp.split("\"")[1]
        while st in messtmp:
            st = messtmp.split("\"")[1]
            messtmp = messtmp.replace("\"" + st + "\"", "")
            if st in messtmp:
                messtmp = messtmp.replace("\"" + st, "")
    words = messtmp.replace("-", " ").replace("  ", " ").split(" ")
    for i in range(0, len(words)):
        word = "".join(re.compile("[\"\'a-zA-Zа-яА-Я0-9 -]").findall(words[i]))
        word = word.lower().replace("a", "а").replace("d", "д").replace("o", "о").replace("y", "у").replace("e", "е")
        if word == name:
            message = message.replace(words[i] + ",", "").replace(words[i], "")
            if i > 0:
                pword = words[i - 1]
                if "," in pword:
                    pword = pword.replace(",", "")
                    message = message.replace(words[i - 1], pword)
    return message.replace("  ", " ").strip()


def processing(message):
    if message in greet:
        print("____________________")
        if (random.randint(0, 1) == 1):
            return randList(greett), ""
    message = message.lower()
    if (message == "нет" or message.split(" ")[-1] == "нет" and random.randint(0, 1) == 1):
        return randList(netotvetlist) + " ответ", ""
    if (random.randint(0, 15) == 8):
        return randList(fcklist), ""
    if (random.randint(3, 8) != 5):
        if '?' in message:
            for q in qlist.keys():
                if q in message:
                    message = randList(globals()[qlist[q]])
                    return message, ""
            message = randList(otheranswer)
            return message, ""
        else:
            for i in resourses.keys():
                if i in message:
                    return globals()[resourses[i]](message)
            if 'ты ' in message or ' ты' in message:
                for i in abusivelist:
                    if i in message:
                        z = random.randint(0, 2)
                        if z == 1:
                            return "Нет, ты " + i, ""
                        elif z == 0:
                            return randList(fcklist), ""
                        else:
                            return i + " ты. И вообще. " + randList(fcklist), ""
            return dickify(message)
    message = message.replace("?", "!")
    return dickify(message)


def wiki(sp):
    if not "интерес" in sp:
        sp = sp.replace("wiki", "").replace("вики", "").replace(",", "").strip()
    else:
        sp = ""
    if not sp:
        s = opentheurl("https://ru.wikipedia.org/w/", "api.php?",
                       [("action", "query"), ("list", "random"), ("prop", "revisions"), ("rvprop", "content"),
                        ("format", "json"), ("rnredirect", "true")])
        title = json.loads(s)["query"]["random"][0]["title"]
    else:
        s = opentheurl("https://ru.wikipedia.org/w/", "api.php?",
                       [("action", "query"), ("srsearch", sp), ("list", "search"), ("format", "json")])
        try:
            title = json.loads(s)["query"]["search"][0]["title"]
        except:
            print("!!!!!!!!!!")
            title = sp
    print(title)
    s1 = opentheurl("https://ru.wikipedia.org/w/", "api.php?",
                    [("action", "query"), ("titles", str(title)), ("prop", "extracts"), ("exintro", "1"),
                     ("format", "xml"), ("redirects", "1"), ("explaintext", "1")])
    page = s1.split("preserve\">")[1].split("</extract>")[0] + "\n\nhttps://ru.wikipedia.org/wiki/" + title.replace(" ", "%20")
    print(page)
    return page,""


# TODO
# def form9gag(page,ptype): f = open ("9gag.html","w"); f.write(page); f.close(); input()
#     page = page.split("<div class=\"badge-post-container post-container \">")[1]
#     while page:
#         post = page.split("<div class=\"badge-post-container post-container \">")[1].split("</header")[0]
#         postlinks.append(post.split("<a href=\"")[1].split("\"")[0])
#         postattachs.append(post.split("src=\"")[1].split("\"")[0])
#         postdiscr.append(post.split("alt=\"")[1].split("\"")[0])
#         posttype.append(post.split("src=\"")[1].split("\"")[0][-3:])
#         page = page.replace("<div class=\"badge-post-container post-container \">"+post+"</header","")
#     i = random.randint(0,len(postlinks)-1)
#     while posttype[i] != ptype:
#         i+=1
#         if i>=(len(postlinks)-1):
#             break
#     return postattaches[i],postdiscr[i]+"\n"+postlinks[i]
#
# def t9gag(message):
#     if "cache" not in os.listdir():
#         os.mkdir("cache")
#     message = message.lower()
#     t = ""
#     for i in t9typelist.keys():
#         if i in message:
#             t = t9typelist[i]
#     c = ""
#     for i in t9catlist:
#         if i in message:
#             c = i
#     link = "http://9gag.com/" + c
#     atlink,message = form9gag(opentheurl(link,"",""),t)
#     if "jpg" in atlink:
#         photo = open("./cache/"+message.split("\n")[0]+".jpg","wb")
#         cont = requests.get(atlink,headers=head)
#         photo.write(cont.content)
#         photo.close()
#         s = opentheurl("https://api.vk.com/method/","photos.getMessagesUploadServer?",[("access_token",token),("v","5.34")])
#         upl = json.loads(s)["response"]["upload_url"]
#         ptf = os.getcwd() + "./cache/" + message.split("\n")[0] + ".jpg"
#         files = {'photo': (message.split("\n")[0]+".jpg", open(r"%s"%path, 'rb'))}
#         s = requests.post(upl,files=files,headers=head)
#         ph = s.json()["photos_list"]
#         s = opentheurl("https://api.vk.com/method/","photos.saveMessagesPhoto?",[("photo",ph),("access_token",token),("v","5.34")])
#         js = s.json
#         attach = "photo" + js["response"][0]["owner_id"] + "_" + js["response"][0]["id"]
#     else:
#         photo = open("./cache/"+message.split("\n")[0]+".mp4","wb")
#         cont = requests.get(atlink,headers=head)
#         photo.write(cont.content)
#         clip = (VideoFileClip("./cache/"+message.split("\n")[0]+".mp4"))
#         clip.write_gif("./cache/"+message.split("\n")[0]+"gif")
#         s = opentheurl("https://api.vk.com/method/","docs.getUploadServer?",[("access_token",token),("v","5.34")])
#         upl = json.loads(s)["response"]["upload_url"]
#         ptf = os.getcwd() + "/cache/" + message.split("\n"[0]) + ".gif"
#         files = {'file': (message.split("\n")[0]+".gif", open(r"%s"%path, 'rb'))}
#         s = requests.post(upl,files=files,headers=head)
#         doc = ph = s.json()["file"]
#         s = opentheurl("https://api.vk.com/method/","docs.save?",[("title",message.split("\n")[0].split(" ")[0]),("file",doc),("access_token",token),("v","5.34")])
#         js = s.json
#         attach = "doc" + js["response"][0]["owner_id"] + "_" + js["response"][0]["id"]
#     os.remove("cache")
#     return message,attach

def marking(mid, mtoken):
    if mid:
        s = opentheurl("https://api.vk.com/method/", "messages.markAsRead?",
                       [("message_ids", mid), ("access_token", str(mtoken))])
        print("Message", mid, "readed")


def control(message, chat):
    if "teamviewer" in message:
        proc = Process(target=TV, args=())
        proc.start()
        scr()
        sendreport("Done!", "/home/bk-201/Code/Ada/cache/screen.jpg", "22709915")
        return "", True
    if "скажи" in message and "\"" in message:
        message = message.split("\"")[1]
        return message, False
    if "позови" in message:
        fname = message.split("позови")[1].strip()
        calling = callsomeone(chat, fname)
        return calling, False
    message = message.lower()
    if (message.split(' ')[-1] in stoplist):
        chatlist.update({str(chat): 1})
        return "someabstractuser", True
    else:
        chatlist.update({str(chat): 0})
        return "someabstractuser", False


def pikabu(ptype):
    t = 0
    if 'текст' in ptype:
        t = 1
    elif 'картин' in ptype:
        t = 2
    elif 'гиф' in ptype:
        t = 3
    elif 'вид' in ptype:
        t = 4
    else:
        t = 0
    i = 0
    s = opentheurl("https://api.vk.com/method/", "wall.get?",
                   [("domain", "pikabu"), ("access_token", token), ("count", 100), ("v", "5.34")])
    allpost = json.loads(s)["response"]
    while True:
        k = random.randint(0, 99)
        post = allpost["items"][k]
        if ("attachments" not in str(post.keys()) and (t == 1 or t == 0)):
            print("-------------->", t)
            print(post["text"], "")
            return post["text"].split("Обсуждение")[0], ""
        elif ("copy_history" in str(post.keys()) and "video" in str(
                post["copy_history"][0]["attachments"][0].keys()) and (t == 4 or t == 0)):
            print("-------------->", t)
            attaches = "video" + str(post["copy_history"][0]["attachments"][0]["video"]["owner_id"]) + "_" + str(
                post["copy_history"][0]["attachments"][0]["video"]["id"])
            print(str(post["copy_history"][0]["text"]), attaches)
            return post["copy_history"][0]["text"].split("Обсуждение")[0], attaches
        elif ("attachments" not in str(post.keys())):
            print("NEW")
        elif ("photo" in str(post["attachments"][0].keys()) and (t == 2 or t == 0)):  # TODO
            print("-------------->", t)
            attaches = ""
            print("\n", post["attachments"], len(post["attachments"]))
            j = 0
            for att in post["attachments"]:
                if "link" in post["attachments"][j]:
                    break
                attaches += "photo"
                attaches += str(post["attachments"][j]["photo"]["owner_id"])
                attaches += ("_")
                attaches += str(post["attachments"][j]["photo"]["id"])
                attaches += (",")
                j += 1
            # attaches = attaches.replace("xxxxxx","")
            print(str(post["text"]), attaches)
            return post["text"].split("Обсуждение")[0], attaches
        elif ("doc" in str(post["attachments"][0].keys()) and (t == 3 or t == 0)):
            attaches = "doc"
            attaches = attaches + str(post["attachments"][0]["doc"]["owner_id"])
            attaches += ("_")
            attaches += str(post["attachments"][0]["doc"]["id"])
            print(str(post["text"]), attaches)
            return post["text"].split("Обсуждение")[0], attaches
        elif ("copy_history" in str(post.keys()) and (t == 4 or t == 0)):
            print("-------------->", t)
            attaches = "video" + str(post["copy_history"][0]["attachments"][0]["video"]["owner_id"]) + "_" + str(
                post["copy_history"][0]["attachments"][0]["video"]["id"])
            print(str(post["text"]), attaches)
            return post["text"].split("Обсуждение")[0], attaches
        elif (i == 200):
            return "Нету нихуя", ""
        else:
            i += 1
            print("NEW")


def bashorg(message):
    i = random.randint(0, 99)
    s = opentheurl("https://api.vk.com/method/", "wall.get?",
                   [("domain", "bashorgruclub"), ("access_token", token), ("offset", i), ("count", 1), ("v", "5.33")])
    post = str(json.loads(s)["response"]["items"][0]["text"])
    return post.split("http")[0].strip(), ""


# TODO
def music(message):
    try:
        s = opentheurl("https://api.vk.com/method/", "audio.search?",
                       [("q", message), ("access_token", token), ("count", 100), ("v", "5.34")])
        count = json.loads(s)["response"]["count"]
        if count >= 99:
            count = 99
        i = random.randint(0, count)
        att = "audio"  # Формируем название аттача (самого аудио)
        att = att + str(json.loads(s)["response"]["items"][i]["owner_id"])  # -||-
        att = att + "_"  # -||-
        att = att + str(json.loads(s)["response"]["items"][i]["id"])
    except:
        time.sleep(1)
        s = opentheurl("https://api.vk.com/method/", "audio.get?",
                       [("owner_id", "22709915"), ("need_user", "0"), ("access_token", token), ("count", 100),
                        ("v", "5.34")])
        count = json.loads(s)["response"]["count"]
        message = "Я не нашла " + randList(thinglist) + ", но вот тебе другая песенка =)"
        if count >= 99:
            count = 99
        i = random.randint(0, count)
        att = "audio"  # Формируем название аттача (самого аудио)
        att = att + str(json.loads(s)["response"]["items"][i]["owner_id"])  # -||-
        att = att + "_"  # -||-
        att = att + str(json.loads(s)["response"]["items"][i]["id"])
    print(att)
    return message, att


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=options[0],
        part="id,snippet",
        maxResults=options[1]
    ).execute()
    videos = []
    channels = []
    playlists = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("(%s)" % (search_result["id"]["videoId"]))
    return randList(videos).replace("(", "").replace(")", "")


def youtube(q):
    print(q)
    try:
        link = "http://www.youtube.com/watch?v=" + youtube_search([str(q), 50])
        print(link)
        s = opentheurl("https://api.vk.com/method/", "video.save?",
                       [("link", link), ("is_private", 1), ("access_token", token), ("v", "5.34")])
        r = requests.get(str(json.loads(s)["response"]["upload_url"]), headers=head)
        att = "video"  # Формируем название аттача (самого аудио)
        att = att + str(json.loads(s)["response"]["owner_id"])  # -||-
        att = att + "_"  # -||-
        att = att + str(json.loads(s)["response"]["video_id"])
        print(att)
        return att
    except Exception as e:
        print(str(e))
        return ""


def friendApprove():
    time.sleep(1)
    opentheurl("https://api.vk.com/method/", "account.setOnline?", [("access_token", token), ("v", "5.34")])
    s = opentheurl("https://api.vk.com/method/", "friends.getRequests?", [("access_token", token), ("v", "5.34")])
    try:
        fr = str(json.loads(s)["response"]["items"][0])
        opentheurl("https://api.vk.com/method/", "friends.add?",
                   [("access_token", token), ("v", "5.34"), ("user_id", fr)])
        print(fr, " added")
    except:
        print("No friends added")


def addusername(usid, message):
    time.sleep(1)
    if usid != '22709915':
        s = opentheurl("https://api.vk.com/method/", "users.get?", [("v", "5.34"), ("user_id", usid), ("lang", "ru")])
        message = str(json.loads(s)["response"][0]["first_name"]) + ", " + message
        return message
    else:
        message = randList(ownerlist) + ", " + message
        return message


def sexcorrect(usid, message):
    time.sleep(1)
    s = opentheurl("https://api.vk.com/method/", "users.get?",
                   [("v", "5.34"), ("user_id", usid), ("lang", "ru"), ("fields", "sex")])
    sex = json.loads(s)["response"][0]["sex"]
    if sex == 1:
        return message.replace("лся", "лась").replace("лся ", "лась ").replace("ал ", "ала ").replace("ыл ",
                                                                                                      "ыла ").replace(
            "сам ", "сама ").replace("лся?", "лась?").replace("ал?", "ала?").replace("ыл?", "ыла?").replace("сам?",
                                                                                                            "сама?").replace(
            "Сам?", "Сама?").replace("Сам ", "Сама ")
    return message


def initiate():
    if random.randint(0, 1) == 0:
        s = opentheurl("https://api.vk.com/method/", "friends.get?", [("access_token", token), ("v", "5.34")])
    else:
        s = opentheurl("https://api.vk.com/method/", "messages.getDialogs?",
                       [("access_token", token), ("v", "5.34"), ("count", 10)])
    items = json.loads(s)["response"]["items"]
    item = randList(items)
    try:
        cid = item["message"]["chat_id"]
        s = opentheurl("https://api.vk.com/method/", "messages.send?",
                       [("message", randList(greett) + " всем"), ("chat_id", cid), ("access_token", token),
                        ("v", "5.34")])
        print(s)
    except:
        uid = item["message"]["user_id"]
        s = opentheurl("https://api.vk.com/method/", "messages.send?",
                       [("message", randList(greett)), ("user_id", uid), ("access_token", token), ("v", "5.34")])
        print(s)


def dosomeshit(message, cd, resp, idofu):
    if (random.randint(0, 15) == 8):
        message = randList(fcklist)
    if (random.randint(0, 10) == 8):
        message = randList(trdlist)
    if (random.randint(0, 9) == 2):
        message = randList(listofgirlshit)
    if (random.randint(0, 17) == 1):
        message = 'И че?'
    if (random.randint(0, 50) == 42):
        slt = random.randint(1, 3600)
        userlist.update({str(idofu): slt})
        message = 'Я обиделась!'
    if (resp):
        message = randList(okaylist)
    if (random.randint(0, 9) == 8):
        message = message + randList(abuselist)
    return message, cd


def lessoffense():
    for i in userlist.keys():
        if userlist[i] > 0:
            userlist[i] -= random.randint(5, 7)
        else:
            userlist[i] = 0


def setact(couid, cu):
    if not cu:
        opentheurl("https://api.vk.com/method/", "messages.setActivity?",
                   [("type", "typing"), ("user_id", couid), ("access_token", token), ("v", "5.34")])
    else:
        opentheurl("https://api.vk.com/method/", "messages.setActivity?",
                   [("type", "typing"), ("chat_id", couid), ("access_token", token), ("v", "5.34")])
    return


def callsomeone(chat_id, firstname):
    s = opentheurl("https://api.vk.com/method/", "messages.getChatUsers?",
                   [("access_token", token), ("chat_id", chat_id), ("v", "5.34"), ("fields", "name"), ("lang", "ru"),
                    ("name_case", "acc")])
    ppl = json.loads(s)["response"]
    for each in ppl:
        if firstname == each["first_name"]:
            if random.randint(0, 1) == 0:
                calling = str(firstname)[:-1] + str(randList(calllist))
                print(calling)
                return calling
            else:
                calling = str(firstname)[:-1] + ", " + str(randList(greett))
                print(calling)
                return calling
    return "Нету тут таких"


def TV():
    os.system('teamviewer')


def scr():
    time.sleep(5)
    os.system('scrot ~/Code/Ada/cache/screen.jpg')
    return


def sendreport(message, adress, user_id):
    time.sleep(0.5)
    s = opentheurl("https://api.vk.com/method/", "photos.getMessagesUploadServer?",
                   [("access_token", token), ("v", "5.34")])
    upl = json.loads(s)["response"]["upload_url"]
    files = {'photo': ("photo.jpg", open(adress, 'rb'))}
    s = requests.post(upl, files=files, headers=head)
    ph = json.loads(s.text)["photo"]
    serv = json.loads(s.text)["server"]
    hsh = json.loads(s.text)["hash"]
    s = opentheurl("https://api.vk.com/method/", "photos.saveMessagesPhoto?",
                   [("hash", hsh), ("server", serv), ("photo", ph), ("access_token", token), ("v", "5.34")])
    js = json.loads(s)
    attach = "photo" + str(js["response"][0]["owner_id"]) + "_" + str(js["response"][0]["id"])
    # print(attach)
    time.sleep(10)
    opentheurl("https://api.vk.com/method/", "messages.send?",
               [("access_token", token), ("v", "5.34"), ("user_id", user_id), ("message", message),
                ("attachment", attach)])


def salt(message):
    # message = "".join(re.compile("[\"\'a-zA-Zа-яА-Я0-9 -]").findall(message))
    # print (message)
    if "соль" in message.lower():
        # print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        c = random.randint(1, 10)
        message = "С"
        while c > 0:
            message = message + "о"
        message = message + "ль"
    return message


def main():
    state = 1
    modeflag = 0
    mode = 0
    counterdesp = 0
    while True:
        say = 'diiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiich'
        stater = 0
        resp = False
        FL = False
        messreserve = ''
        mid = ''
        try:
            # deltamorning = myunitime(str(datetime.now().date())+str(morningtime)) - myunitime(str(datetime.now())[:-7])
            # if (deltamorning <=0):
            # if random.randint(0, 4095)==42:
            # initiate()
            time.sleep(random.randint(1, 3))
            s = opentheurl("https://api.vk.com/method/", "messages.get?",
                           [("count", 10), ("filters", 1), ("out", 0), ("v", "5.4"), ("access_token", token)])
            items = json.loads(s)["response"]["items"]
            items.reverse()
            lessoffense()
            for item in items:
                # print(item[""])
                attid = ""
                mess = item["body"]
                messbuff = mess
                idofu = str(item["user_id"])
                try:
                    userid = item["chat_id"]
                    mid = item["id"]
                    FL = True
                    name = accost(mess)
                    mess = rname(mess, name)
                    messbuff = mess
                    if name:
                        print("To me")
                        setact(userid, FL)
                        if (idofu == '22709915' and mode == 0):
                            say, resp = control(mess, userid)
                    else:
                        print("Not to me")
                        stater = 1
                except:
                    userid = item["user_id"]
                    mid = item["id"]
                    FL = False
                    setact(userid, FL)
                    say, resp = control(mess, userid)
                state = chatlist.get(str(userid))
                offense = userlist.get(str(idofu))
                print(offense)
                if ((stater != 1 and state != 1 and str(userid) != "305193192" or resp) and not offense):
                    if mode == 0:
                        for i in modes.keys():
                            if i in mess.lower():
                                print("MODE")
                                modeflag = modes[i]
                                mess = "Конкретнее"
                                break
                        if say.split(",")[0] not in mess:
                            if modeflag == 0:
                                mess, attid = processing(str(mess))
                                # print("-->",mess)
                            if not mess:
                                mess = randList(notunderst)
                        else:
                            mess = say
                    elif mode == 1:
                        mess, attid = music(str(mess))
                        modeflag = 0
                    elif mode == 2:
                        attid = youtube(str(mess))
                        if not attid:
                            mess = "Я не нашла " + randList(thinglist)
                        modeflag = 0
                    mess, counterdesp = dosomeshit(mess, counterdesp, resp, idofu)
                    mess = sexcorrect(idofu, mess)
                    if messbuff in callfrommemory(idofu) and random.randint(0, 1):
                        mess = randList(repeatlist)
                    keepinmemory(messbuff, idofu)
                    while (len(mess) >= 4095):
                        time.sleep(1)
                        messbuff = mess[:4095]
                        messreserve = mess[-(len(mess) - len(messbuff)):]
                        mess = messbuff
                        print(mess, "\n------------\n", messreserve)
                        if FL:
                            if mess not in trdlist and "ru.wikipedia.org" not in mess and say.split(",")[0] not in mess:
                                mess = mess[:1].lower() + mess[-(len(mess) - 1):]
                                mess = addusername(idofu, mess)
                            s = opentheurl("https://api.vk.com/method/", "messages.send?",
                                           [("chat_id", userid), ("attachment", str(attid)), ("message", str(mess)),
                                            ("access_token", token)])
                        else:
                            s = opentheurl("https://api.vk.com/method/", "messages.send?",
                                           [("user_id", userid), ("attachment", str(attid)), ("message", str(mess)),
                                            ("access_token", token)])
                        # print (s)
                        mess = messreserve
                    time.sleep(1)
                    if FL:
                        if mess not in trdlist and "ru.wikipedia.org" not in mess and say.split(",")[0] not in mess:
                            mess = mess[:1].lower() + mess[-(len(mess) - 1):]
                            mess = addusername(idofu, mess)
                        s = opentheurl("https://api.vk.com/method/", "messages.send?",
                                       [("chat_id", userid), ("attachment", str(attid)), ("message", str(mess)),
                                        ("access_token", token)])
                    else:
                        s = opentheurl("https://api.vk.com/method/", "messages.send?",
                                       [("user_id", userid), ("attachment", str(attid)), ("message", str(mess)),
                                        ("access_token", token)])
                    # print (s)
                    friendApprove()
                print("<~>-<~>-<~>-<~>-<~>-<~>-<~>-<~>-<~>-<~>")
                if ('Я обиделась!' in mess or 'я обиделась!' in mess and random.randint(0, 4) == 2):
                    # time.sleep(slt)
                    akfhsgdf = 1
                mode = modeflag
                time.sleep(random.randint(0, 2))
            marking(mid, token)
            mid = ''
        except Exception as e:
            print(str(e))
            time.sleep(random.randint(10, 20))
            continue


if __name__ == '__main__':
    main()
