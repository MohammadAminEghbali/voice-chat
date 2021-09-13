from pyrogram import Client, filters
from pyrogram.types import Message

help_text = """
راهنمای دستورات ربات:
╼╾╼╾╼*╾╼╾╼╾
```!play``` (روی یک موزیک ریپلای کنید)
⁉️ پخش موزیک،
درصورتی که موزیکی پخش میشد به پلی لیست اضافه میشه موزیک
╼╾╼╾╼╾╼╾╼╾╼╾
```!stop```
⁉️ متوقف کردن چت صوتی،
در این حالت ربات از چت صوتی خارج میشه و کل پلی لیست حذف میشه
╼╾╼╾╼╾╼╾╼╾╼╾
```!pause```
⁉️ متوقف کردن موزیک
╼╾╼╾╼╾╼╾╼╾╼╾ 
```!resume```
⁉️ از سر گیری پخش موزیک
╼╾╼╾╼╾╼╾╼╾╼╾
```!skip```
⁉️ در صورتی که موزیکی درحال پخش بود میره موزیک بعد
╼╾╼╾╼╾╼╾╼╾╼╾
```!volume``` (یک عدد بین 0 تا 200)
⁉️ تنظیم صدای پخش
"""


@Client.on_message(
    ~filters.edited &
    ~filters.linked_channel &
    filters.command("help", '!')
)
async def helper(app:Client, msg:Message):
    return await msg.reply(help_text)