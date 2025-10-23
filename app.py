from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# あなたのLINEチャネル情報を入れてください
LINE_CHANNEL_ACCESS_TOKEN = 'PScoiVPg444zmlwxHhFKTsuj9TDPvn29Fx8+xAFJM8trbKUtDFE8GkTAaQZ7hzdwRbs0XMZycY/9K/zJXgyQQiGzg5WtHv19LK6GpnUF/s8b0G6KWnS5iqQ0/bIkFTVt3XRONe+KYNAef2Q14vWhYQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '55eeed31b958afb87727ba5829771123'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

last_char = ''

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global last_char
    user_msg = event.message.text.strip()

    if last_char and user_msg[0] != last_char:
        reply_text = "違うよ"
    else:
        if user_msg[-1] == 'ん':
            reply_text = "あなたの負け"
            last_char = ''
        else:
            reply_text = f"{user_msg[-1]}あ"
            last_char = reply_text[-1]
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = reply_text)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
