import asyncio
import websockets
import json
import requests
from datetime import datetime
import os

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

def format_timestamp(unix_time):
    dt = datetime.utcfromtimestamp(unix_time)
    return dt.strftime("%Y-%m-%d %H:%M UTC")

async def post_to_telegram(news):
    title = news.get("news_title", "No Title")
    coins = ", ".join(news.get("coins_included", []))
    url = news.get("url", "")
    time = format_timestamp(news.get("timestamp", 0))

    message = f"🗞 <b>{title}</b>\n🪙 <b>Coins:</b> {coins}\n⏰ <b>Time:</b> {time}\n🔗 <a href='{url}'>Read more</a>"

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(telegram_url, data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    })

async def listen_news():
    uri = "wss://bwenews-api.bwe-ws.com/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            news = json.loads(data)
            await post_to_telegram(news)

asyncio.run(listen_news())
