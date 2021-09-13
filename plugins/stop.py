import asyncio
from os import remove

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory

from .db import *


@Client.on_message(~filters.edited & filters.command('stop', '!'))
async def stoper(app:Client, msg:Message):
    chat_id = msg.chat.id
    group_call = active_calls.get(chat_id)
    
    if group_call:
        await asyncio.sleep(2)
        del active_calls[chat_id], calls[chat_id]
        group_call.input_filename = None
        group_call.stop_playout()
        await group_call.stop()
        group_name = f'chat|{msg.chat.id}'
        lastfile = redis.hget(str(chat_id), 'lastfile')
        if lastfile:
            remove(lastfile.decode())
        redis.delete(str(chat_id), group_name)
        return await msg.reply('چت صوتی پایان یافت')
    
    else:
        return await msg.reply('''
ربات در چت صوتی نیست
میتوانید با ریپلای روی یک موزیک و فرستادن 
```!play```
موزیک مورد نظر خود را پخش کنید
''')
