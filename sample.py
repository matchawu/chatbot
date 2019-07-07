from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN='bJHk54azcb7mtSNkJ4Q3Gw5wL0dXrH1n7BW04Fuf7tkm/Tg3rQP8iaB3sxh8n3GWFLmlXxyUpCGiY0/NFM14jn0yS5K+QOMua3e+7m0NU9oXP+8i25qqfYDiD/cWBzP4CVJ69Y7iiwZ9DDHf6A1TfgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET='c766ecfe8812c2c528aba688c208db38'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 使用heroku的environment variables
# line_bot_api = LineBotApi(os.environ['bJHk54azcb7mtSNkJ4Q3Gw5wL0dXrH1n7BW04Fuf7tkm/Tg3rQP8iaB3sxh8n3GWFLmlXxyUpCGiY0/NFM14jn0yS5K+QOMua3e+7m0NU9oXP+8i25qqfYDiD/cWBzP4CVJ69Y7iiwZ9DDHf6A1TfgdB04t89/1O/w1cDnyilFU='])
# handler = WebhookHandler(os.environ['c766ecfe8812c2c528aba688c208db38'])


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應使用者輸入的話
    # message = TextSendMessage(text='Hello, world')
    # line_bot_api.reply_message(event.reply_token, message)
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

    message = ImageSendMessage(
        original_content_url='https://example.com/original.jpg',
        preview_image_url='https://example.com/preview.jpg'
    )
    line_bot_api.reply_message(event.reply_token, message)

    message = VideoSendMessage(
        original_content_url='https://example.com/original.mp4',
        preview_image_url='https://example.com/preview.jpg'
    )
    line_bot_api.reply_message(event.reply_token, message)

    message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )
    line_bot_api.reply_message(event.reply_token, message)

    # {
    #     "to": "U4f16834ed145e0893ea5e48b0227bdc1",
    #     "messages": [
    #         {
    #             "type": "text",
    #             "text": "Hello,這是測試訊息喔"
    #         },
    #         {
    #             "type":"sticker",
    #             "packageId": "1",
    #             "stickerId": "2"
    #         }
    #     ]
    # }


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Setting host='0.0.0.0' will make Flask available from the network
    app.run(host='0.0.0.0', port=port)
