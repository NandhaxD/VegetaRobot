import random
from VegetaRobot import telethn as tbot
from telethon import events
@tbot.on(events.NewMessage(pattern="/wish"))
async def wish(vegeta):
         mm = random.randint(1,100)
         VEGETA = "https://telegra.ph/file/68be46bb292a9230a584b.jpg"
         await tbot.send_file(vegeta.chat_id, VEGETA,caption=f"**Your wish has been cast.✨**\n__chance of success {mm}%__", reply_to=lol,file=VEGETA)
        #thanks to @h0daka for image
      #Codes by @Tamilvip008
#Kang With Else Gay
