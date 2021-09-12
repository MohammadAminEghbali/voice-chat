import asyncio
from os import mkdir, path, remove

import ffmpeg
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import CreateGroupCall, GetGroupCall
from pyrogram.raw.types import ChannelFull, InputChannel
from pyrogram.types import Message, User
from pytgcalls import GroupCallFactory

from .db import *
from .utils import *


audio_filter = filters.create(audio)

@Client.on_message(~filters.edited & ~filters.linked_channel & filters.command('play', '!') & audio_filter)
async def player(app:Client, msg:Message):
    chat_id = msg.chat.id
    chat_str = str(chat_id)
    group_name = f'chat|{chat_id}'
    
    if redis.hget(chat_str, 'playing') == None:
        redis.hset(chat_str, 'playing', 1)
        chat_path = f'./groups/{chat_id}/'

        if calls.get(chat_id):
            group_call = calls.get(chat_id)

        else:
            calls[chat_id] = (group_call := GroupCallFactory(app).get_file_group_call())

        msg_result:Message = await msg.reply("درحال برسی اطلاعات چت")

        peer = await app.resolve_peer(chat_id)
        call = (await app.send(
            GetFullChannel(
                channel=InputChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash
                )
            )
        )).full_chat.chat_info.call 

        if call == None:
            await msg_result.edit("چت صوتی یافت نشد درحال ساخت چت صوتی")
            crearte = await create_vc(app, msg)
            if crearte != True:
                return None
        
        await msg_result.edit("درحال آماده سازی موزیک موردنظر")

        if not path.exists(chat_path):
            mkdir(chat_path)
    
        input_file = await msg.reply_to_message.download(chat_path)
        raw_file = create_random_raw_name(input_file)
        convert = await convertor(input_file, raw_file)
        remove(input_file)
        
        if convert:
            await msg_result.edit("عملیات باموفقیت انجام شد")
            await msg.delete()
            
            redis.hset(chat_str, 'lastfile', raw_file)
            await set_call_file(group_call, raw_file) 
            
            active_calls[chat_id] = group_call
            
            await group_call.start(chat_id)
            
                                    
            @group_call.on_playout_ended
            async def queue(_, __):
                lastfile = redis.hget(chat_str, 'lastfile')
                if lastfile:
                    remove(lastfile.decode())
                    redis.hdel(chat_str, 'lastfile')
                        
                if lrange(group_name) != [] and redis.hget(chat_id, 'skiping') == None:
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

                        return await msg.edit('موزیک طبق پلی لیست به این موزیک تغییر کرد')
                    
                else:
                    redis.delete(chat_str)
                    await app.send_message(chat_id, 'تمامی موزیک ها پایان یافتند و موزیکی برای پخش موجود نیست')
                    del calls[chat_id]
                    del active_calls[chat_id]
                    return await group_call.stop()
                
        else:
            redis.hdel(chat_str, 'playing')
            return await msg_result.edit('خطا در آماده سازی موزیک'), await msg.delete()
    
    else:
        await msg.reply("موزیک به صف موزیک ها اضافه شد")
        await msg.delete()
        return lpush(group_name, msg.reply_to_message.message_id)
            