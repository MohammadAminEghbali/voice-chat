from pyrogram import Client, filters
from pyrogram.types import Message

from .db import active_calls

@Client.on_message(~filters.edited & ~filters.linked_channel & filters.command('volume','!'))
async def pauser(app:Client, msg:Message):
    if len(msg.command) == 2:
        chat_id = msg.chat.id
        group_call = active_calls.get(chat_id)
        volume = 1
        try:
            # volume = int(msg.command[1]) & float(msg.command[1])
            volume = float(msg.command[1])
        
        except ValueError:
            return await msg.reply('میزان صدا اشتباه وارد شده است')
        
        if group_call and volume != None:
            return (
                await group_call.set_my_volume(volume),
                await msg.reply(f"میزان صدا به {volume:.0f} تغییر کرد"),
                await msg.delete()
            )
        
        else:
            return (
                await msg.reply("موزیکی از قبل پخش نمیشد"),
                await msg.delete()
            )
    
    else:
        return await msg.reply("""
فرمت دستور اشتباه است
دستور به شکل زیر باید باشد:
```!volume``` **num**
بجای num یک عدد بین 0 تا 200 قرار دهید
""")