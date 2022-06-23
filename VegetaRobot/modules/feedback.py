from VegetaRobot import pgram as bot, SUPPORT_CHAT
from pyrogram import filters
import random
from datetime import datetime
from pyrogram.types import *

#made by t.me/nandhaxd

vegeta_img = [ "https://telegra.ph/file/03ba8fea3c3ed2b98b68a.jpg", 
"https://telegra.ph/file/be242e647504b5b253f79.jpg",
"https://telegra.ph/file/51323082ef6051f3a9721.jpg",
"https://telegra.ph/file/072bc7f5f9fdf7f04acb3.jpg"]

@bot.on_message(filters.group & filters.command(["feedback","bug"]))
async def feedback(_, m):
         if len(m.command) < 2:
               await m.reply_text("**Gime a Feedback!**")
               return 
         text = m.text.split(None, 1)[1]
         user = m.from_user
         chat = m.chat
         datetimes_fmt = "%d-%m-%Y"
         datetimes = datetime.utcnow().strftime(datetimes_fmt)
         feedback = f""" **#NewFeedBack**
FromChat: @{chat.username}
user_id: {user.id}
mention: {user.mention}
msg_date: {datetimes}
Feedback: **{text}**
"""      
         msg = await bot.send_photo(f"@{SUPPORT_CHAT}",random.choice(vegeta_img),caption=feedback,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "➡ View Report", url=f"{m.link}"),
                            InlineKeyboardButton(
                                "❌ Close", callback_data="close")
                        ]
                    ]
                )
            )
    

         await m.reply_text("Your feedback Successfully Reported On SupportChat!",
                    reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "➡ View Report", url=f"{msg.link}")]]))
         
