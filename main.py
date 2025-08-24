from telethon.sync import TelegramClient
from telethon.tl.types import Message
import json
from config import API_ID, API_HASH, SESSION_NAME, GROUP_USERNAME
from zoneinfo import ZoneInfo


SG_TIMEZONE = ZoneInfo("Asia/Singapore")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def export_messages():
    messages = []
    async for msg in client.iter_messages(GROUP_USERNAME):
        if msg.message and msg.message.lower().startswith("drabroski quest submission"):
            messages.append({
                "id": msg.id,
                "sender_id": msg.sender_id,
                "text": msg.message,
                "date": msg.date.astimezone(SG_TIMEZONE).isoformat(),
                "media": bool(msg.media)
            })

    with open("data/raw_messages.json", "w") as f:
        json.dump(messages, f, indent=2)

with client:
    client.loop.run_until_complete(export_messages())
