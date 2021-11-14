import html
import random
import re

import requests as r
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import escape_markdown


from VegetaRobot import DEMONS, DRAGONS, dispatcher
from VegetaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from VegetaRobot.modules.helper_funcs.alternate import typing_action
from VegetaRobot.modules.helper_funcs.extraction import extract_user


@run_async
@typing_action
def goodnight(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"Good Night! {escape_markdown(first_name)}"
    message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


@run_async
@typing_action
def goodmorning(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"Good Morning! {escape_markdown(first_name)}"
    message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

    __mod_name__="😂Funs"
    
GOODMORNING_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(gm|good morning)"), goodmorning, friendly="goodmorning"
)
GOODNIGHT_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(gn|good night)"), goodnight, friendly="goodnight"
)
dispatcher.add_handler(GOODMORNING_HANDLER)
dispatcher.add_handler(GOODNIGHT_HANDLER)
