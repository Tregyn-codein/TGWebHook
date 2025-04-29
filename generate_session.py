from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Session string:", client.session.save())