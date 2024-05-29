from time import sleep
from typing import Optional, List
from telegram import TelegramError
from telegram import Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import Filters, CommandHandler
from telegram.ext.dispatcher import run_async, CallbackContext

import random
import VegetaRobot.modules.sql.users_sql as sql
from VegetaRobot.modules.helper_funcs.filters import CustomFilters
from VegetaRobot import dispatcher, OWNER_ID, LOGGER
from VegetaRobot.modules.disable import DisableAbleCommandHandler
USERS_GROUP = 4


def send(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        message_text = ''.join(str(args[1:]))
        if not message_text:
            update.effective_message.reply_text(
            "Please give me a message text to echo!")
    except:
        update.effective_message.reply_text(
            "Please give me a chat and message text to echo!")
    to_send = message_text
    try:
        chat = bot.getChat(chat_id)
        bot.sendMessage(chat.id, str(to_send))
        update.effective_message.reply_text(
              f"*Successfully message sent to {chat.title}*"
            , parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                f"❌ Errors occur: `{e}`"
            )


__help__ = """

──「 *Sudo only:* 」──
-> /send <chat> <string>
Make me send a message to a specific chat.
"""

__mod_name__ = "Send"

SNIPE_HANDLER = CommandHandler(
    "send",
    send,
    pass_args=True,
    filters=CustomFilters.sudo_filter, run_async=True)

dispatcher.add_handler(SNIPE_HANDLER)
