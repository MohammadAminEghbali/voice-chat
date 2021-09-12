from pyrogram import Client, filters
from pyrogram.types import Message

from pytgcalls import GroupCallFactory

from .db import *

@Client.on_message(~filters.edited & filters.command('stop', '!'))
async def stoper(app:Client, msg:Message):
    chat_id = msg.chat.id
    group_call = active_calls.get(chat_id)
    
    if group_call:
        await group_call.stop()
        del active_calls[chat_id]
        group_name = f'chat|{msg.chat.id}'
        redis.delete(str(chat_id), group_name)
        return await msg.reply('چت صوتی پایان یافت')
    
    else:
        return await msg.reply('''
ربات در چت صوتی نیست
میتوانید با ریپلای روی یک موزیک و فرستادن 
```!play```
موزیک مورد نظر خود را پخش کنید
''')