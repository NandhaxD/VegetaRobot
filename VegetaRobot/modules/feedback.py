
from pyrogram import filters, types, enums, errors
from VegetaRobot import pgram, JOIN_LOGGER, OWNER_USERNAME, SUPPORT_CHAT



@pgram.on_message(filters.command(["bug", "feedback"]))
async def BugsReport(bot, message):
         m = message
         if not len(m.text.split()) >= 2:
             return await m.reply_text(
                   "⚡ **Offer us any requests for new module or report any bugs using the command:** `/bug text`"
             )
         if not m.from_user: return
                  
         user_id = m.from_user.id
         mention = m.from_user.mention
         date = m.date
         bug_text = (
f"""                 
⚡ **By**: {mention}
🆔 **Id**: `{user_id}`
📆 **Date**: `{date}`

{ f"🔗 **Link**: {m.link}" if m.chat.type != enums.ChatType.PRIVATE else ""}

🐞 **Bug Msg**:
```
{m.text.split(maxsplit=1)[1]}
```
"""
         )                  
         
         try:
             BugMsg = await bot.send_message(
             chat_id=JOIN_LOGGER, # send bug report to channel
             text=bug_text
                )
         except:
             return await bot.send_message(
                  chat_id=OWNER_USERNAME, # if bot can't access channel then send to owner
                  text=bug_text
             )
         ReportMsg = await bot.send_message(
                      chat_id=SUPPORT_CHAT,
                      text = (
                      
f"""
**⚡ Someone reported a bug in {bot.me.mention}
Please checkout and assist them.** ✨

Check here: **[Bug report]({BugMsg.link})**
"""
)
             )
         return await m.reply_text(
             text = (
           "**⚡ Successfully the report has been sent to Support chat click the below to view and wait for the answer 🐼.**"           
         ), reply_markup=types.InlineKeyboardMarkup([[
                  types.InlineKeyboardButton(
                           "👁️", url=ReportMsg.link
                  )
         ]])
         )
         
                  
         
         
         
