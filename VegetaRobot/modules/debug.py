import datetime
import os

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telethon import events

from VegetaRobot import dispatcher, telethn
from VegetaRobot.modules.helper_funcs.chat_status import dev_plus

DEBUG_MODE = False

@dev_plus
def getdebug(u: Update, c: CallbackContext):
    global DEBUG_MODE

    msg = u.effective_message
    if DEBUG_MODE:
     
        file = "updates.txt"
        path = os.path.exists(file)
        if path:
            msg.reply_document(
               document=open(path, 'rb')
            )
        else:
            msg.reply_text("🤔 It seems the path doesn't exist")
    else:
        msg.reply_text(
           "please enable the debug mode to receive the file!"
        )
         



@dev_plus
def debug(update: Update, context: CallbackContext):
    global DEBUG_MODE
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message
    print(DEBUG_MODE)
    if len(args) > 1:
        if args[1] in ("yes", "on"):
            DEBUG_MODE = True
            message.reply_text("Debug mode is now on.")
        elif args[1] in ("no", "off"):
            DEBUG_MODE = False
            message.reply_text("Debug mode is now off.")
    else:
        if DEBUG_MODE:
            message.reply_text("Debug mode is currently on.")
        else:
            message.reply_text("Debug mode is currently off.")


@telethn.on(events.NewMessage(pattern="[/!].*"))
async def i_do_nothing_yes(event):
    global DEBUG_MODE
    if DEBUG_MODE:
        print(f"-{event.from_id} ({event.chat_id}) : {event.text}")
        if os.path.exists("updates.txt"):
            with open("updates.txt", "r") as f:
                text = f.read()
            with open("updates.txt", "w+") as f:
                f.write(text + f"\n-{event.from_id} ({event.chat_id}) : {event.text}")
        else:
            with open("updates.txt", "w+") as f:
                f.write(
                    f"- {event.from_id} ({event.chat_id}) : {event.text} | {datetime.datetime.now()}"
                )


@dev_plus
def logs(update: Update, context: CallbackContext):
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message
    with open("log.txt", "rb") as f:
        context.bot.send_document(
            document=f, 
            filename=f.name,
            chat_id=chat.id,
            reply_to_message_id=message.message_id
        )


LOG_HANDLER = CommandHandler("logs", logs, run_async=True)
DEBUG_HANDLER = CommandHandler("debug", debug, run_async=True)
GETDEBUG_HANDLER = CommandHandler("getdebug", getdebug, run_async=True)


dispatcher.add_handler(LOG_HANDLER)
dispatcher.add_handler(DEBUG_HANDLER)
dispatcher.add_handler(GETDEBUG_HANDLER)



__mod_name__ = "Debug"
__command_list__ = ["debug", "getdebug"]
__handlers__ = [DEBUG_HANDLER, GETDEBUG_HANDLER]
