import html
import random
import time

from telegram import ParseMode, Update, ChatPermissions
from telegram.ext import CallbackContext, run_async
from telegram.error import BadRequest

import VegetaRobot.modules.memes_strings as memes_strings
from VegetaRobot import dispatcher
from VegetaRobot.modules.disable import DisableAbleCommandHandler
from VegetaRobot.modules.helper_funcs.chat_status import (is_user_admin)
from VegetaRobot.modules.helper_funcs.extraction import extract_user

@run_async
def memes(update: Update, context: CallbackContext):
    message = update.effective_message
    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    reply_photo = message.reply_to_message.reply_photo if message.reply_to_message else message.reply_photo
    reply_photo(
        random.choice(memes_strings.MEMES_IMG))

__help__ = """
 '/memes`*:* gives random anime quotes **(:**
 `/memeCreat`*:* {text} created your meme **(:**
 
"""
MEMES_HANDLER = DisableAbleCommandHandler("memes", memes)

dispatcher.add_handler(MEMES_HANDLER)

__mod_name__ = "🔥MemeFun"
__command_list__ = [
    "memes"
]
__handlers__ = [
    MEMES_HANDLER
]
