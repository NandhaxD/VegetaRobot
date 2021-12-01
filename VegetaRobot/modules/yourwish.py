import random
from VegetaRobot import telethn as tbot
from telethon import events
@tbot.on(events.NewMessage(pattern="/wish"))
async def wish(vegeta):
   if not vegeta.is_reply:
         mm = random.randint(1,100)
         VEGETA = "https://telegra.ph/file/68be46bb292a9230a584b.jpg"
         await tbot.send_file(vegeta.chat_id, VEGETA,caption=f"**Your wish has been cast.✨**\n__chance of success {mm}%__", reply_to=lol,file=VEGETA)
        #thanks to AASF and h0daka for image
      #Codes by @Tamilvip008
#it you going to kang this module dont remove this crdits..
