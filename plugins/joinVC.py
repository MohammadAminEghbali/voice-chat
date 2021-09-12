# from pyrogram import Client, filters
# from pyrogram.raw.functions.phone import CreateGroupCall
# from pyrogram.types import Message
# from pyrogram.raw.types import InputPeerChannel
# from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
# from pytgcalls import GroupCallFactory
# from pytgcalls.exceptions import GroupCallNotFoundError
# from os import path

# from .utils import create_vc

# @Client.on_message(filters.command("join", '!'))
# async def joinvc(app:Client, msg:Message):
#     chat_id = msg.chat.id
#     group_call = GroupCallFactory(app).get_file_group_call()
    
#     try:
#         await group_call.start(chat_id)
    
#     except GroupCallNotFoundError:
#         create = await create_vc(app, msg)
        
#         if create == True:
#             await group_call.start(chat_id)
#             await msg.reply("ربات با موفقیت در چت صوتی عضو شد")

#     else:
#        await msg.reply("ربات با موفقیت در چت صوتی عضو شد")