import random
from VegetaRobot import telethn as tbot
from telethon import events

@tbot.on(events.NewMessage(pattern="/wish"))
async def wish(event):
   if event.is_reply:
         mm = random.randint(1,100)
         lol = await event.get_reply_message()
         await tbot.send_message(event.chat_id, f"**Your wish has been cast.✨**\n\n__chance of success {mm}%__", reply_to=lol)
   if not event.is_reply:
         mm = random.randint(1,100)
         VEGETA = "https://telegra.ph/file/68be46bb292a9230a584b.jpg"
         await tbot.send_file(event.chat_id, VEGETA, f"**Your wish has been cast.✨**\n\n__chance of success {mm}%__", reply_to=e)
        
   
        #thanks to AASF for image
      #Codes by @Tamilvip008
#Kang With Else Gay
