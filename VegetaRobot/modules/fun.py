

import requests
import os

from VegetaRobot import dispatcher
from VegetaRobot.modules.disable import DisableAbleCommandHandler

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html





def emojimix(u: Update, c: CallbackContext):
    msg = u.effective_message
    user = u.effective_user
    chat = u.effective_chat
  
    if len(msg.text.split()) == 2:
        emoji_1, emoji_2 = msg.text.split()[1].split("+")
        api_url = "https://apis-awesome-tofu.koyeb.app/api/emojimix?emoji1={}&emoji2={}".format(emoji_1, emoji_2)
        path = f"{user.id}{chat.id}.webp"
        response = requests.get(api_url)
        if response.status_code == 200:
             with open(path, 'wb+') as f:
                f.write(response.content)
             ok = msg.reply_sticker(
                sticker=open(path, 'rb')
             )
             if ok:
                os.remove(path)
             
        else:
             msg.reply_text(f"❌ Status: {response.status_code}")
        
    else:
        return msg.reply_text(
           "Sorry wrong format pal! do like: /emojimix 😊+🐼")
     
 
        


def truth(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply = msg.reply_to_message
    chat = update.effective_chat
    user = update.effective_user
    if not reply or (reply and not reply.from_user):
        msg.reply_text("Reply to the user ❗")
    else:
        user = msg.from_user
        ruser = reply.from_user
        
        rmention = mention_html(ruser.id, ruser.first_name)
        mention = mention_html(user.id, user.first_name)

        api_url = "https://nandha-api.onrender.com/truth"
        response = requests.get(api_url)
        if response.status_code != 200:
           msg.reply_text("❌ Something went wrong in API please vist support chat")
       
        text = response.json()['truth']
        reply.reply_text(
          text = ( 
            f"<b>Hey {rmention}, {mention} asked a truth question to you ( ꈍᴗꈍ) !!!</b>\n\n"
            f"𝗧𝗥𝗨𝗧𝗛: <code>{text}</code>"
          ), parse_mode=ParseMode.HTML
         )
        

def dare(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply = msg.reply_to_message
    chat = update.effective_chat
    user = update.effective_user
    if not reply or (reply and not reply.from_user):
        msg.reply_text("Reply to the user ❗")
    else:
        user = msg.from_user
        ruser = reply.from_user
        
        rmention = mention_html(ruser.id, ruser.first_name)
        mention = mention_html(user.id, user.first_name)

        api_url = "https://nandha-api.onrender.com/dare"
        response = requests.get(api_url)
        if response.status_code != 200:
           msg.reply_text("❌ Something went wrong in API please vist support chat")
       
        text = response.json()['dare']
        reply.reply_text(
          text = ( 
            f"<b>Hey {rmention}, {mention} asked a dare question to you ( ꈍᴗꈍ) !!!</b>\n\n"
            f"𝗗𝗔𝗥𝗘: <code>{text}</code>"
          ), parse_mode=ParseMode.HTML
         )
        

TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth, run_async=True)                          
DARE_HANDLER = DisableAbleCommandHandler("dare", dare, run_async=True)
EMOJIMIX_HANDLER = DisableAbleCommandHandler("emojimix", emojimix, run_async=True)



dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
dispatcher.add_handler(EMOJIMIX_HANDLER)



__mod_name__ = "Fun"

__command_list__ = [
  'truth', 'dare', 'emojimix'
]


__help__ = """
➪ /truth: reply to someone for ask truth's
➪ /dare: reply to someone for ask dare's
➪ /emojimix 🐼+😊: to combine two emojis
"""
