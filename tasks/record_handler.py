# -*- coding: utf-8 -*-
from celery import Celery
from celery.contrib.methods import task_method
import celeryconfig
from parse_json import MessageHandler
import requests #POST / GETとか送る用のモジュールはこれでいいのか

celery = Celery('TodoTask')
celery.config_from_object(celeryconfig)

# added by KanU
LINE_ENDPOINT = "sth"
HEADERS = {
    "X-Line-ChannelID": "1463141779", #channel id
    "X-Line-ChannelSecret": "781410f0c7180dd6c7cdd609dc673746", #channel secret
    "X-Line-Trusted-User-With-ACL": "u5a4a644eb5f3dec17bffa4c007fe5603" #channel mid
}
EVENTTYPE = {
    "message" : "138311609100106303",
    "other" : "138311609100106403",
}
CONTENTTYPE = {
    "text" : 1,
    "image" : 2,
    "video" : 3,
    "audio" : 4,
    "location" : 7,
    "sticker" : 8,
}

# データ処理は全てここで行う
class TodoTask(object):
    def __init__(self):
        pass

    # added by : Kan
    @celery.task(filter=task_method, name='TodoTask.run')
    def call(self, obj_cls, data):
        req = data[result][0]

        #友達登録 / テキストのメッセージを受信 / それ以外　で分類
 
        #友達登録時
        if req["eventType"] == EVENTTYPE["other"] and req["content"]["opType"] == 4 :
            text = u"友達登録ありがとうございます。あなただけの秘書です。"
            to = req["from"]
            send(to, CONTENTTYPE["text"],text=text)
            
            return

        #受信したテキストメッセージを json_parse に流す
        elif req["eventType"] == EVENTTYPE["message"] and req["content"]["contentType"] == 1:
            messages = req["content"]["text"]
            user_id = req["content"]["from"]
            handler = MessageHandler(message,user_id)
            
            return

        #それ以外（画像等 or Block）
        #Blockの時、無駄な反応しちゃうけどそれでいのー？
        else :
            text = u"ごめんね、文字じゃないと分からないの。 '登録'・'削除'・'表示'のどれかを入力してちょーだい。"
            to = [req["content"]["from"]]
            send(to,CONTENTTYPE["text"],text=text)
            
            return

        return 

    @celery.task(filter=task_method, name='TodoTask.create')
    def create(self, obj_cls, **kwargs):
        todo = obj_cls.objects.create(kwargs)

        return todo.title

    #added by : Kan
    #contentTypeを呼び出すときは上述の定数CONTENTYPEを使う
    def send(to, contentType, **kwargs):
        app.logger.info(content)
        data = {
            "to": to,
            "toChannel": "1383378250",
            "eventType": "138311608800106203",
            "content": format_content(contentType, kwargs),
        }

        r = requests.post(LINE_ENDPOINT + "/v1/events", json=data, headers=HEADERS)
        app.logger.info(r.text)


    # added by : Kan
    # ユーザーにtextメッセージを送る時の処理
    def format_content(contentType, properties):
        content = {
            "contentType": contentType,
            "toType": 1, #Fixed value
        }.update(properties)
        return content

