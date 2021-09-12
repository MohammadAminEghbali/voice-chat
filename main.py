from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import GetMessages
from pyrogram.raw.types import InputPeerChat, InputMessageID
from os import path, mkdir

if not path.exists("groups"):
    mkdir("groups")


app = Client(
    'BAAZPpvYFWMaPA_OWQ4erActtuQnywFWV5IIReNwA4kEDLuQ7KDfDxjWUKFvHyex68B9qow-wBX9NF1ffzz8G8rSUH8WNL8q86MQJbbEB84e6AmQFxjhJwmccN7FsFAiBPvpyDRybC8cU2OUttZthXIH2ZgaLH3M5mB8CfrK-4c7gjOKCzz0oi3bR0QpbVo1MxLXf389guRQ9JwgMAkh8BWgYIKZ67XuJsWvJ5TPE-k_sLxuwZgovN8ndork3vxK2ix-l_MdNOP-MQLR9PfRaYr5_eP7xb7BLVNt_Y60zdymtrRf1nMoF4G8D1y1al8gVy9388qkPwilkScacUymjXWWcyQMpwA',
    6,
    'eb06d4abfb49dc3eeb1aeb98ae0f581e',  
    plugins={'root':'plugins'}
)


app.run()