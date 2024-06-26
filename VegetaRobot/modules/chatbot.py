
from pyrogram import filters, types, enums, errors
from VegetaRobot import aiohttpsession as session, pgram, BOT_ID
from VegetaRobot.modules.sql import chatbot_sql as sql




async def get_response(prompt: str) -> str:
    url = "https://nandha-api.onrender.com/nandhaai"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "text": prompt,
        "role": "You're a helpful assistant chatbot, you're name Vegeta, you're personality looks like Vegeta from dragon balls"
    }
    
    async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("reply")
            else:
                return None


@pgram.on_message(filters.command("chatbot"))
async def ChatBot(bot, message):
     m = message
     admin_ids = []
     ok = False
     if m.chat.type == enums.ChatType.PRIVATE:
          ok = True
     if not ok:
          async for mem in bot.get_chat_members(
              chat_id=m.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
          ):
                 admin_ids.append(mem.user.id)
          if not m.from_user.id in admin_ids:
              return await m.reply_text(
                  "Sorry you're not authorized to do this. only admin can!"
              )
          else:
              return await m.reply_text(
                 text="⚡ **Chat Bot Settings**",
                 reply_markup=types.InlineKeyboardMarkup([[
                   types.InlineKeyboardButton(
                     text="🟢", callback_data=f"chatbot:enable:{m.from_user.id}"
                   ),
                   types.InlineKeyboardButton(
                     text="🔴", callback_data=f"chatbot:disable:{m.from_user.id}"
                   )
                 ]])
              )
     else:
         return await m.reply_text(
                 text="⚡ **Chat Bot Settings**",
                 reply_markup=types.InlineKeyboardMarkup([[
                   types.InlineKeyboardButton(
                     text="🟢", callback_data=f"chatbot:enable:{m.from_user.id}"
                   ),
                   types.InlineKeyboardButton(
                     text="🔴", callback_data=f"chatbot:disable:{m.from_user.id}"
                   )
                 ]])
         )


@pgram.on_message(group=33)
async def ChatBotReply(bot, message):
     m = message
     reply = m.reply_to_message
     if reply and reply.from_user and reply.from_user.id == BOT_ID:
          chat_id = m.chat.id
          if sql.is_kuki(chat_id):
               prompt = m.text
               response = await get_response(prompt)
               if response:
                   await bot.send_chat_action(
                     chat_id, enums.ChatAction.TYPING
                   )
                   return await m.reply_text(
                         text=response
                         )




@pgram.on_callback_query(filters.regex(r"^chatbot"))
async def ChatBot_CQ(bot, query):
      user_id = int(query.data.split(':')[2])
      mod = query.data.split(':')[1]
      m = query.message
      if query.from_user.id != user_id:
          return await query.answer(
              text="This is not requested by you ⚡", show_alert=True
          )
      else:
          if mod == 'enable':
              is_kuki = sql.set_kuki(m.chat.id)
              return await m.edit_text(
                f"⚡ **Chat bot Successfully added 🟢 in {m.chat.title if m.chat.title else m.chat.first_name} by {query.from_user.mention}**"
              )
          elif mod == 'disable':
              is_kuki = sql.rem_kuki(m.chat.id)
              return await m.edit_text(
                f"⚡ **Chat bot Successfully removed 🔴 in {m.chat.title if m.chat.title else m.chat.first_name} by {query.from_user.mention}**"
              )
          else:
              return await query.answer(
                  text='Callback data #404 no mod type 🤔', show_alert=True
              )
                                                                                                                 
                  
     
