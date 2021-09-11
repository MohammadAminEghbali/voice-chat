from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.raw.functions.phone import GetGroupCall, CreateGroupCall
import ffmpeg

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
    # if not path.exists(raw_file):
    #     open(raw_file, 'w').close()
    
    try:
        ffmpeg.input(input_file).output(
            raw_file,
            format='s16le',
            acodec='pcm_s16le',
            ac=2, ar='48k'
        ).overwrite_output().run(quiet=True)
        
    except:
        return False
    
    else:
        return True
    
# def get_duration(input_file):
#     try:
#         duration = int(float(ffmpeg.probe(input_file)['streams'][0]['duration']))
#     except:
#         return None
    
#     else:
#         return duration
    

# def filter_user(_, __, msg):
#     if msg.chat.type == 'channel':
#         return True