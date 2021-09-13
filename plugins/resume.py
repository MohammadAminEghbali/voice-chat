from pyrogram import Client, filters
from pyrogram.types import Message

from .db import active_calls

@Client.on_message(
    ~filters.edited &
    ~filters.linked_channel &
    ~filters.private &
    filters.command('resume','!')
)
async def pauser(app:Client, msg:Message):
    chat_id = msg.chat.id
    group_call = active_calls.get(chat_id)

    if group_call:
        group_call.enable_action = True
        return (
            group_call.resume_playout(),
            await msg.reply('موزیک دوباره اجرا شد'),
            await msg.delete()
        )
    
    else:
        return (
            await msg.reply("موزیکی از قبل پخش نمیشد"),
            await msg.delete()
        )