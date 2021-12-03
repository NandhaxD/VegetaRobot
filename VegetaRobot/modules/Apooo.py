import random
from VegetaRobot.events import register
from VegetaRobot import telethn

IDK_IMG="https://telegra.ph/file/561fa547f3c4940c95ddf.jpg"
APAKAH_STRING = ["Iya", 
                 "Tidak", 
                 "Mungkin", 
                 "Mungkin Tidak", 
                 "Bisa jadi", 
                 "Mungkin Tidak",
                 "Tidak Mungkin",
                 "YNTKTS",
                 "Pala bapak kau pecah",
                 "Apa iya?",
                 "Tanya aja sama mamak kau tu pler"
                 ]


@register(pattern="^/apakah ?(.*)")
async def apakah(event):
    quew = event.pattern_match.group(1)
    if not quew:
        await event.reply('Berikan saya pertanyaan 😐')
        return
    await event.reply_photo(IDK_IMG,random.choice(APAKAH_STRING))
