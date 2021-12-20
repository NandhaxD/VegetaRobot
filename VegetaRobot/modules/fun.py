#this module only Created in @VegetaRobot ©pegasusXteam

import html
import random
import re

import requests as r
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import escape_markdown

import VegetaRobot.modules.fun_strings as fun
from VegetaRobot import DEMONS, DRAGONS, dispatcher, SUPPORT_CHAT
from VegetaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from VegetaRobot.modules.helper_funcs.alternate import typing_action
from VegetaRobot.modules.helper_funcs.extraction import extract_user

GN_IMG= "https://telegra.ph/file/6b67b1f44a669a634cab8.jpg"

@run_async
@typing_action
def goodnight(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"*Hey {escape_markdown(first_name)} \nGood Night! 😴*"
    message.reply_photo(GN_IMG,reply, parse_mode=ParseMode.MARKDOWN)

GM_IMG= "https://telegra.ph/file/e3b27f1b746344c8fdb28.jpg"
@run_async
@typing_action
def goodmorning(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"*Hey {escape_markdown(first_name)} \n Good Morning!☀*"
    message.reply_photo(GM_IMG,reply, parse_mode=ParseMode.MARKDOWN)

    
@run_async
def gbun(update, context):
    user = update.effective_user
    chat = update.effective_chat

    if update.effective_message.chat.type == "private":
        return
    if int(user.id) in DRAGONS or int(user.id) in DEMONS:
        context.bot.sendMessage(chat.id, (random.choice(fun.GBUN)))


@run_async
def gbam(update, context):
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    message = update.effective_message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        gbam_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(gbam_user.first_name)

    else:
        user1 = curr_user
        user2 = bot.first_name

    if update.effective_message.chat.type == "private":
        return
    if int(user.id) in DRAGONS or int(user.id) in DEMONS:
        gbamm = fun.GBAM
        reason = random.choice(fun.GBAM_REASON)
        gbam = gbamm.format(user1=user1, user2=user2, chatid=chat.id, reason=reason)
        context.bot.sendMessage(chat.id, gbam, parse_mode=ParseMode.HTML)
        
@run_async
def yesnowtf(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    res = r.get("https://yesno.wtf/api")
    if res.status_code != 200:
        return msg.reply_text(random.choice(fun.DECIDE))
    else:
        res = res.json()
    try:
        context.bot.send_animation(
            chat.id, animation=res["image"], caption=str(res["answer"]).upper()
        )
    except BadRequest:
        return
        
@run_async
@typing_action
def repo(update, context):
    update.effective_message.reply_text(fun.REPO)
  
@run_async
def insult(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.SFW_STRINGS))
    else:
      message.reply_text(random.choice(fun.SFW_STRINGS)) 
    
    
@run_async
def abuse(update, context):
    context.bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(fun.ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(fun.ABUSE_STRINGS))

@run_async
@typing_action
def truth(update, context):
    update.effective_message.reply_text(random.choice(fun.TRUTH))

@run_async
@typing_action
def tamilmeme(update, context):
    update.effective_message.reply_photo(random.choice(fun.TAMIL_MEME))


@run_async
@typing_action
def dare(update, context):
    update.effective_message.reply_text(random.choice(fun.DARE))
 
@run_async
def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(fun.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(fun.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(fun.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)
                                                                     
            
    
GOODMORNING_HANDLER = DisableAbleMessageHandler(Filters.regex(r"(?i)(goodmorning|good morning)"), goodmorning, friendly="goodmorning")
GOODNIGHT_HANDLER = DisableAbleMessageHandler(Filters.regex(r"(?i)(goodnight|good night)"), goodnight, friendly="goodnight")
REPO_HANDLER = DisableAbleCommandHandler("repo", repo)
YESNOWTF_HANDLER = DisableAbleCommandHandler("decide", yesnowtf)
GBUN_HANDLER = CommandHandler("gbun", gbun)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
GBAM_HANDLER = CommandHandler("gbam", gbam)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)
TAMILMEME_HANDLER = DisableAbleCommandHandler("tamilmeme", tamilmeme)
TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
INSULT_HANDLER = DisableAbleCommandHandler("insult", insult)
ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)

dispatcher.add_handler(GOODMORNING_HANDLER)
dispatcher.add_handler(GOODNIGHT_HANDLER)
dispatcher.add_handler(INSULT_HANDLER)
dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(GBAM_HANDLER)
dispatcher.add_handler(GBUN_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(YESNOWTF_HANDLER)
dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(REPO_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
dispatcher.add_handler(TAMILMEME_HANDLER)

__help__ = f"""
This Module credits by @VegetaRobot
*`Goodnight`|`goodmorning`
bot send GM or GN image,*
/decide - bot send radom decides.
/pat - reply to user.
/truth or /dare - bot send funny messages.
/insult - bot send insult message.
/abuse - bot send abuse message.
/tamilmeme - get meme for tami language.
report bug - 
@{SUPPORT_CHAT}`
"""

__mod_name__ = "😁Fun"


#guys this it you like pegasusXteam ask join @pegasusSupportofficial
# © pegasusXteam
