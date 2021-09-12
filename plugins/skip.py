from os import remove, path

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory

from .db import *
from .utils import *


@Client.on_message(~filters.edited & ~filters.linked_channel & filters.command('skip', '!'))
async def skiper(app:Client, msg:Message):
    chat_id = msg.chat.id
    group_call = active_calls.get(chat_id)
    
    await msg.delete()
    
    if group_call:
        group_name = f'chat|{chat_id}'
        chat_path = f'./groups/{chat_id}/'
        chat_str = str(chat_id)
        
        if lrange(group_name) != []:
            lastfile = redis.hget(chat_str, 'lastfile')
            if lastfile and path.exists(lastfile.decode()):
                remove(lastfile.decode())
                redis.hdel(chat_str, 'lastfile')
                
            redis.hset(chat_str, 'skiping', 1)
            msg_id = int(lpop(group_name, True))
            msg = await app.send_message(
                chat_id,
                'درحال آماده سازی موزیک جدید',
                reply_to_message_id=msg_id
            )
            
            try:
                input_file = await (
                    await app.get_messages(chat_id, msg_id)
                    ).download(chat_path)
            
            except ValueError:
                return await msg.edit('موزیک پیدا نشد')
            
            else:
                raw_file = create_random_raw_name(input_file)
                await convertor(input_file, raw_file)
                
                await set_call_file(group_call, raw_file)
                remove(input_file)
                
                redis.hset(chat_str, 'lastfile', raw_file)

                return (
                    await msg.edit('موزیک طبق پلی لیست به این موزیک تغییر کرد'),
                    redis.hdel(chat_str, 'skiping')
                    )
            
        else:
            return await app.send_message(chat_id, 'تمامی موزیک ها پایان یافتند و موزیکی برای پخش موجود نیست')
        
    else:
        return await msg.reply('چت صوتی وجود ندارد')
