import asyncio
from random import randint
from os import path

import ffmpeg
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.raw.functions.phone import CreateGroupCall, GetGroupCall
from pyrogram.types import Message

from .db import redis


async def create_vc(app:Client, msg:Message):
    chat_id = msg.chat.id
    rnd = app.rnd_id()
    peer = await app.resolve_peer(chat_id)

    try:
        await app.send(
            CreateGroupCall(
                peer=peer,
                random_id=rnd // 9000000000
            )
        )
        
    except ChatAdminRequired:
        await msg.reply("متاسفانه ربات در گروه مدیر نیست یا دسترسی ساخت چت صوتی را ندارد\nشما میتوانید به صورت دستی چت صوتی راه اندازی کنید\nیا اینکه به ربات دسترسی های لازم را بدهید")
        return False

    else:
        return True
   
            
async def convertor(input_file, raw_file):
    command = f'ffmpeg -i "{input_file}" -f s16le -ac 2 -ar 48000 -acodec pcm_s16le "{raw_file}" -hide_banner'
    
    commandline = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    _, *__ = await commandline.communicate()
    
    if path.exists(raw_file):
        return True
    
    else:
        return False
    
    
def create_random_raw_name(input_name):
    return f'{input_name}{randint(randint(10, 100), randint(110, 200))}.raw'


async def set_call_file(call, file):
    call.input_filename = file
    return None


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
