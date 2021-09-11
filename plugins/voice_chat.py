# from pyrogram import Client
# from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
# from pyrogram.raw.functions.phone import CreateGroupCall, GetGroupCall
# from pyrogram.types import Message
# from pytgcalls import GroupCallFactory


# class PyroGroupCall(GroupCallFactory):
#     def __init__(self, client, **kargs):
#         self.client = client
#         super().__init__(self.client, **kargs)
#         self.group_call = self.get_group_call()
#         self.group_call.start_video()

#     async def join(self):
#         pass
    
#     async def create(self):
#         pass
    