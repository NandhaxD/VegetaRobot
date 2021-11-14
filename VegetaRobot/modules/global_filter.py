
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import escape_markdown
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update

from VegetaRobot.modules.helper_funcs.alternate import typing_action

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
