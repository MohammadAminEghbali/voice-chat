from pyrogram import Client, filters
from pyrogram.types import Message

from .db import active_calls

@Client.on_message(~filters.edited & ~filters.linked_channel & filters.command('pause','!'))
async def pauser(app:Client, msg:Message):
    chat_id = msg.chat.id
    group_call = active_calls.get(chat_id)

    if group_call:
        return (
            group_call.pause_playout(),
            await msg.reply('موزیک متوقف شد'),
            await msg.delete()
        )
    
    else:
        return (
            await msg.reply("موزیکی از قبل پخش نمیشد"),
            await msg.delete()
        )