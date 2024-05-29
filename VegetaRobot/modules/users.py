from io import BytesIO
from time import sleep

from telegram import TelegramError, Update, ParseMode
from telegram.error import BadRequest, Unauthorized
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, run_async)

import VegetaRobot.modules.sql.users_sql as sql
from VegetaRobot import DEV_USERS, LOGGER, OWNER_ID, dispatcher, pgram
from VegetaRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from VegetaRobot.modules.sql.users_sql import get_all_users


from pyrogram import filters, types

import asyncio

USERS_GROUP = 4
CHAT_GROUP = 5
DEV_AND_MORE = DEV_USERS.append(int(OWNER_ID))


def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith('@'):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = dispatcher.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    LOGGER.exception("Error extracting user ID")

    return None




@pgram.on_message(filters.user(OWNER_ID) & filters.command(
  ['bcastgroup','bcastuser', 'fbcastgroup','fbcastuser']
))
async def broadcast(bot: pgram, message: types.Message):
   m = message
   reply = m.reply_to_message
   command = m.command[0]
   chat_id = m.chat.id
   is_forward = command.startswith('f')
   is_group = command.endswith('group')
   is_user = command.endswith('user')
   done = 0
  
   if not reply:
         return await message.reply_text(
           text='Reply to the message for produce a broadcast!'
         )
   failed_chat, failed_user = 0, 0

   msg = await m.reply_text('Broadcasting...') 
   if is_group:
        chats = sql.get_all_chats() or []


        for chat in chats:


            done += 1
          
            if done % 5 == 0:
                  await msg.edit_text(f'**Successfully broadcast sent to {done} chats loop processing. ❤️**.')
                  await asyncio.sleep(5)
            try:
                await (bot.forward_messages if is_forward else bot.copy_message)(
                    int(chat.chat_id),
                    chat_id,
                    reply.id
                )
                
            except Exception:
                failed_chat += 1

   if is_user:
        users = sql.get_all_users() or []
        for user in users:

            done += 1
            if done % 5 == 0:
                  await msg.edit_text(
                    f"Successfully broadcast sent to {done} group chats and loop processing..."
                  )
                  await asyncio.sleep(5)
              
            try:
                await (bot.forward_messages if is_forward else bot.copy_message)(
                    int(user.user_id),
                    chat_id,
                    reply.id
                )
                
            except Exception:
                failed_user += 1
   await msg.edit_text(
        f"**Broadcast completed!**\n**Failed Users**: {failed_user}\n**Failed Chats**: {failed_chat}"
    )
        
        

@dev_plus
def fbroadcast(update: Update, context: CallbackContext):
    message = update.effective_message
    reply = message.reply_to_message
    chat = update.effective_chat
  
    chat_id = chat.id
    to_send = message.text.split(None, 1)

    
    if reply:
        to_group = False
        to_user = False
        if to_send[0] == '/fbroadcastgroups':
            to_group = True
        if to_send[0] == '/fbroadcastusers':
            to_user = True
        else:
            to_group = to_user = True
        chats = sql.get_all_chats() or []
        users = get_all_users()
        failed_chat = 0
        failed_user = 0
        if to_group:
            for chat in chats:
                try:
                    context.bot.forward_message(
                        chat_id=int(chat.chat_id),
                        from_chat_id=chat_id,
                        message_id=reply.message_id
                    )
                    sleep(0.6)
                except TelegramError:
                    failed_chat += 1
        if to_user:
            for user in users:
                try:
                    context.bot.forward_message(
                        chat_id=int(user.user_id),
                        from_chat_id=chat_id,
                        message_id=reply.message_id
                    )
                    sleep(0.6)
                except TelegramError:
                    failed_user += 1
        update.effective_message.reply_text(
            f"*Broadcast complete.*\n*Groups failed*: {failed_chat}.\n*Users failed*: {failed_user}."
        , parse_mode=ParseMode.MARKDOWN)
    else:
      return message.reply_text(
         "Reply to the message for produce a broadcast message!"
    )



@dev_plus
def broadcast(update: Update, context: CallbackContext):
    message = update.effective_message
    reply = message.reply_to_message
    
    to_send = message.text.split(None, 1)

    message_text = reply.text if reply else to_send[1]
  
    if (reply and reply.text) or len(to_send) >= 2:
        to_group = False
        to_user = False
        if to_send[0] == '/broadcastgroups':
            to_group = True
        if to_send[0] == '/broadcastusers':
            to_user = True
        else:
            to_group = to_user = True
        chats = sql.get_all_chats() or []
        users = get_all_users()
        failed_chat = 0
        failed_user = 0
        if to_group:
            for chat in chats:
                try:
                    context.bot.sendMessage(
                        int(chat.chat_id),
                        message_text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True)
                    sleep(0.6)
                except TelegramError:
                    failed_chat += 1
        if to_user:
            for user in users:
                try:
                    context.bot.sendMessage(
                        int(user.user_id),
                        message_text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True)
                    sleep(0.6)
                except TelegramError:
                    failed_user += 1
        update.effective_message.reply_text(
            f"*Broadcast complete.*\n*Groups failed*: {failed_chat}.\n*Users failed*: {failed_user}."
        , parse_mode=ParseMode.MARKDOWN)
    else:
      return message.reply_text(
         "Reply to the message or gimme a text message to produce a broadcast message!"
    )


def log_user(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message

    sql.update_user(msg.from_user.id, msg.from_user.username, chat.id,
                    chat.title)

    if msg.reply_to_message:
        sql.update_user(msg.reply_to_message.from_user.id,
                        msg.reply_to_message.from_user.username, chat.id,
                        chat.title)

    if msg.forward_from:
        sql.update_user(msg.forward_from.id, msg.forward_from.username)


@sudo_plus
def chats(update: Update, context: CallbackContext):
    all_chats = sql.get_all_chats() or []
    chatfile = 'List of chats.\n0. Chat name | Chat ID | Members count\n'
    P = 1
    for chat in all_chats:
        try:
            curr_chat = context.bot.getChat(chat.chat_id)
            bot_member = curr_chat.get_member(context.bot.id)
            chat_members = curr_chat.get_members_count(context.bot.id)
            chatfile += "{}. {} | {} | {}\n".format(P, chat.chat_name,
                                                    chat.chat_id, chat_members)
            P = P + 1
        except:
            pass

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "groups_list.txt"
        update.effective_message.reply_document(
            document=output,
            filename="groups_list.txt",
            caption="Here be the list of all groups in my database.")


def chat_checker(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        if update.effective_message.chat.get_member(
                bot.id).can_send_messages is False:
            bot.leaveChat(update.effective_message.chat.id)
    except Unauthorized:
        pass


def __user_info__(user_id):
    if user_id in [777000, 1087968824]:
        return """╘══「 Groups count: <code>???</code> 」"""
    if user_id == dispatcher.bot.id:
        return """╘══「 Groups count: <code>???</code> 」"""
    num_chats = sql.get_user_num_chats(user_id)
    return f"""╘══「 Groups count: <code>{num_chats}</code> 」"""


def __stats__():
    return f"• {sql.num_users()} users, across {sql.num_chats()} chats"


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


BROADCAST_HANDLER = CommandHandler(
    ["broadcastall", "broadcastusers", "broadcastgroups"], broadcast, run_async=True)
FBROADCAST_HANDLER = CommandHandler(
    ["fbroadcastall", "fbroadcastusers", "fbroadcastgroups"], fbroadcast, run_async=True)

USER_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups, log_user, run_async=True)
CHAT_CHECKER_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups, chat_checker, run_async=True)
CHATLIST_HANDLER = CommandHandler("groups", chats, run_async=True)

dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(BROADCAST_HANDLER)
dispatcher.add_handler(FBROADCAST_HANDLER)
dispatcher.add_handler(CHATLIST_HANDLER)
dispatcher.add_handler(CHAT_CHECKER_HANDLER, CHAT_GROUP)

__handlers__ = [(USER_HANDLER, USERS_GROUP), BROADCAST_HANDLER, FBROADCAST_HANDLER,
                CHATLIST_HANDLER]
