from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
import random
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('fPfNtUK5wPi7PcBXmWdxrluZDTZu8wJqOsQyqOa1QtQkpfvf3k1dHsxsFeqYFkRL2R794KRwinoSVujKGuQUuxN9lZmgdlUoZDLWFL5ADdLyZVpBvgHzL+FSTPxAUGN3wDHFqnJH1OGZV933Ur1DdgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f69a5d9c9ec821a28c91ea7ea7a4e545')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    msg = "火焰車輪餅\n" + "營業時間: 18:00~22:00\n" + "距離: 100m\n" + "地址導航: https://google.com" + \
        " \n\n-------------------\n\n" + \
        "無情香腸攤\n" + "營業時間: 18:00~22:00\n" + "距離: 200m\n" + "地址導航: https://google.com" + " \n\n-------------------\n\n" + \
        "街頭藝人 - 大衛\n" + "表演時間: 18:00~22:00\n" + "距離: 300m\n" + "地址導航: https://google.com" + " \n\n-------------------\n\n" + "地圖連結: https://google.com"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = msg))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '地點' in msg:
        shops = [
            {
                "title": "火焰車輪餅",
                "time": "18:00~22:00",
            },
            {
                "title": "無情香腸攤",
                "time": "18:00~22:00",
            },
            {
                "title": "太神啦水果攤",
                "time": "18:00~22:00",
            },
            {
                "title": "街頭藝人 - 大爺",
                "time": "10:00~12:00",
            },
            {
                "title": "街頭藝人 - 大衛",
                "time": "12:00~22:00",
            },
            {
                "title": "街頭藝人 - 董神",
                "time": "07:40~01:40",
            },
            {
                "title": "街頭藝人 - 力量人",
                "time": "12:55~22:55",
            },
            {
                "title": "街頭藝人 - 黃老師",
                "time": "12:00~22:00",
            },
            {
                "title": "7-11 X shop",
                "time": "12:00~22:00",
            },
            {
                "title": "2022創客松",
                "time": "00:00~23:59",
            }
        ]
        random_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(random_index)

        message = ""
        for i in range(3):
            index = random_index[i]
            message += f'{shops[index]["title"]}\n' + f'營業時間: {shops[index]["time"]}\n' + \
                f'距離: {int((i + 1) * 100)}m\n' + "地址導航: https://google.com" + " \n\n-------------------\n\n"
        message += "地圖連結: https://google.com"
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = message))
    
    elif '使用說明' in msg:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = " \
                                        按鈕功能 >>\n\n\
                                        \
                                        目前區域附近商家: \n\
                                            點按「地點」\n\n\
                                        \
                                        上架自己的資訊: \n\
                                            點按「上傳/更新」\n\n\
                                        \
                                        快速查詢(待更新) >>\n\n\
                                        \
                                        尋找特定商家: \n\
                                            [攤販名稱]\n\n\
                                        \
                                        尋找特定街頭藝人: \n\
                                            [街頭藝人姓名]\
                                        "))


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)



@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
