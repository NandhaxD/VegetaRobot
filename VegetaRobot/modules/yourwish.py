/eval import random
from VegetaRobot import telethn as asst
from telethon import events
@asst.on(events.NewMessage(pattern="/wish"))
async def wish(e):
   if e.is_reply:
         mm = random.randint(1,100)
         lol = await e.get_reply_message()
         await asst.send_message(e.chat_id, f"**Your wish has been cast.✨**\n\n__chance of success {mm}%__", reply_to=lol)
   if not e.is_reply:
         mm = random.randint(1,100)
         await asst.send_message(e.chat_id, f"**Your wish has been cast.✨**\n\n__chance of success {mm}%__", reply_to=e)
        
        #© @pegasusXteam
