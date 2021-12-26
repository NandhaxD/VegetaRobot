import random
from telegram import Update
from telegram.ext import CallbackContext, run_async
from VegetaRobot import dispatcher
from telegram.utils.helpers import escape_markdown
from VegetaRobot.modules.helper_funcs.alternate import typing_action
from VegetaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler

WISH_IMG="https://telegra.ph/file/5c1f2e655a539c7f8b2be.jpg"
@run_async
@typing_action
def wish(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    wishchoice = f"Hey! {escape_markdown(first_name)}\nYour Wish Possible to 25%😟",f"Hey! {escape_markdown(first_name)}\nYour Wish Possible to 50%🤔",f"Hey! {escape_markdown(first_name)}\nYour Wish Possible to 75%😉",f"Hey! {escape_markdown(first_name)}\nYour Wish Possible to 100%😍"
    message.reply_photo(WISH_IMG,random.choice(wishchoice))

WISH_HANDLER = DisableAbleCommandHandler("wish", wish) 

dispatcher.add_handler(WISH_HANDLER)   

#module Creat by @ctzfamily

__help__="""
 • /wish - reply your wish message.
 bot send Your Wish Possible to random numbers. 😃
 Module Creat by @Ctzfamily
"""



__mod_name__="🎄Wish"
