from random import randint

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
   
            
def convertor(input_file, raw_file):
    try:
        ffmpeg.input(input_file).output(
            raw_file,
            format='s16le',
            acodec='pcm_s16le',
            ac=2, ar='48k'
        ).overwrite_output().run(quiet=True)
        
    except Exception as e:
        print(e)
        return False
    
    else:
        return True
    
    
def create_random_raw_name(input_name):
    return f'{input_name}{randint(randint(10, 100), randint(110, 200))}.raw'


def set_call_file(call, file):
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