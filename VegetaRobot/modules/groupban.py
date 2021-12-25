from io import BytesIO
from time import sleep
from typing import Optional, List
from telegram import TelegramError, Chat, Message
from telegram import Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown
from VegetaRobot.modules.helper_funcs.chat_status import is_user_ban_protected, user_admin

import random
import telegram
import VegetaRobot.modules.sql.users_sql as sql
from VegetaRobot import dispatcher, OWNER_ID, DRAGONS, DEMONS, LOGGER
from VegetaRobot.modules.helper_funcs.filters import CustomFilters
from VegetaRobot.modules.disable import DisableAbleCommandHandler
USERS_GROUP = 4

def banall(update, context):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        all_mems = sql.get_chat_members(chat_id)
    else:
        chat_id = str(update.effective_chat.id)
        all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text("Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(excp.message + " " + str(mems.user))
            continue

BANALL_HANDLER = CommandHandler("banall", banall, pass_args=True)

dispatcher.add_handler(BANALL_HANDLER)
