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

class TodoTask(object):
    def __init__(self):
        pass

    # added by : Kan
    @celery.task(filter=task_method, name='TodoTask.run')
    def call(self, obj_cls, data):
        req = data[result][0]

        #友達登録 / テキストのメッセージを受信 / それ以外　で分類
 
        #友達登録時
        if req["eventType"] == "138311609100106403" && req["content"]["opType"] == 4 :
            text = u"友達登録ありがとうございます。あなただけの秘書です。"
            send_text(req['from'], text)

        #受信したテキストメッセージを json_parse に流す
        elif req["eventType"] == "138311609000106303" && req["content"]["contentType"] == 1:
            messages = req["content"]["text"]
            user_id = req["content"]["from"]
            handler = MessageHandler(message,user_id)

        #それ以外（画像等 or Block）
        #Blockの時、無駄な反応しちゃうけどそれでいのー？
        else :
            text = u"ごめんね、文字じゃないと分からないの。 '登録'・'削除'・'表示'のどれかを入力してちょーだい。"
            to = [req["content"]["from"]]
            send_text(to,text)

        return 'task {0}'.format(data)

    @celery.task(filter=task_method, name='TodoTask.create')
    def create(self, obj_cls, **kwargs):
        todo = obj_cls.objects.create(**kwargs)

        return todo.title

    # added by : Kan
    # ユーザーにtextメッセージを送る時の処理
    def send_text(to, text):
        content = {
            "contentType": 1,
            "toType": 1,
            "text": text
        }
        events(to, content)

    #added by : Kan
    def events(to, content):
        app.logger.info(content)
        data = {
            "to": to,
            "toChannel": "1383378250",
            "eventType": "138311608800106203",
            "content": content
        }

        r = requests.post(LINE_ENDPOINT + "/v1/events", json=data, headers=HEADERS)
        app.logger.info(r.text)