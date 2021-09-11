import asyncio
from os import path, remove
# from time import sleep
from threading import Thread

import ffmpeg
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import CreateGroupCall, GetGroupCall
from pyrogram.raw.types import ChannelFull, InputChannel
from pyrogram.types import Message, User
from pytgcalls import GroupCallFactory

from .db import *
from .joinVC import joinvc
from .utils import convertor, create_vc


async def audio(_, __, msg:Message):
    text = 'لطفا روی یک فایل موسیقی ریپلای کنید'
    if await filters.reply(Client, msg):
        if msg.reply_to_message.audio:
            return True
        else:
            await msg.reply(text)
            return False
    else:
        await msg.reply(text)
        return False

audio_filter = filters.create(audio)


@Client.on_message(filters.command('play', '!') & audio_filter)
async def player(app:Client, msg:Message):
    chat_id = msg.chat.id
    group_name = f'chat|{msg.chat.id}'

    if calls.get(chat_id):
        group_call = calls.get(chat_id)

    else:
        calls[chat_id] = (group_call := GroupCallFactory(app).get_file_group_call(play_on_repeat=False))
        # calls[chat_id] = group_call
    
    if redis.hget(f'{chat_id}', 'playing') == None:
        redis.hset(f'{chat_id}', 'playing', 1)
        redis.hset(f'{chat_id}', 'request', 1)

        msg_result:Message = await msg.reply("درحال برسی اطلاعات گروه و چت صوتی ...")

        peer = await app.resolve_peer(chat_id)
        chat_info = (await app.send(
            GetFullChannel(
                channel=InputChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash
                )
            )
        )).full_chat
        
        call = chat_info.call
        check_me = False
        
        if call == None:
            await msg_result.edit("چت صوتی یافت نشد!\nدر حال ساخت چت صوتی")
            crearte = await create_vc(app, msg)
            if crearte != True:
                return None
        
        else:
            my_id = (await app.get_me()).id
            
            call = await app.send(GetGroupCall(
                call=call
            ))
            
            for i in call.users:
                if my_id == i.id:
                    check_me = True
                    break
        
        await msg_result.edit("در حال آماده سازی موزیک مورد نظر")

        
        input_file = await msg.reply_to_message.download('./')
        raw_file = f'{input_file}.raw'
        convert = convertor(input_file, raw_file)
        
        
        if convert:
            await msg_result.edit("عملیات با موفقیت به اتمام رسید\nاز موسیقی لذت ببرید")
            
            group_call.input_filename = raw_file
            
            if check_me == False:
                await group_call.start(chat_id)
                # await group_call.start_audio(input_file)
                
            redis.hdel(f'{chat_id}', 'request')
            
            @group_call.on_playout_ended
            async def x(_, __):
                print(lrange(group_name))
                if lrange(group_name) != []:
                    msg_id = int(lpop(group_name, True))
                    _msg:Message = await (await app.get_messages(chat_id, msg_id)).download('./')
                    
                    raw_file = _msg + '.raw'
                    convertor(_msg, raw_file)
                    group_call.input_filename = raw_file
                    
                    await group_call.start(chat_id)
                    return await app.send_message(chat_id,
                        'موزیک طبق پلی لیست به این موزیک تغییر کرد',
                        reply_to_message_id=msg_id)
                
                else:
                    print('bye')
                    redis.hdel(f'{chat_id}', 'playing')
                    await group_call.stop()
                    return await app.send_message(chat_id, 'موسیقی تمام شد و موسیقیی در صف پخش موجود نیست')
                
        else:
            return await msg_result.edit('خطا در آماده سازی موسیقی')
    
    else:
        if redis.hget(f'{chat_id}', 'request') == None:
            await msg.reply("یک موزیک در حال پخش است\nموسیقی مورد نظر به صف موزیک های گروه اضافه شد")
            lpush(group_name, msg.reply_to_message.message_id)
                  
        else:
            return await msg.reply("شما یک درخواست نا تمام دارید\nلطفا تا پایان آن منتظر بمانید")