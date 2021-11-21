from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import GetMessages
from pyrogram.raw.types import InputPeerChat, InputMessageID
from os import path, mkdir

if not path.exists("groups"):
    mkdir("groups")


app = Client(
    'bot',
    6,
    'eb06d4abfb49dc3eeb1aeb98ae0f581e',  
    plugins={'root':'plugins'}
)

app.run()