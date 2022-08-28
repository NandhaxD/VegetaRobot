from VegetaRobot import pgram as bot
from pyrogram import filters
from pyrogram.types import *

SOURCE_IMAGE = "http://telegra.ph/file/e4781c5d359939627904d.jpg"

SOURCE_TEXT = """**Hello!  Searching for Vegeta's Repository?
We're kindly asking Vegeta have Some Errors! But it's Also have some good modules you can use your bots to are else you can run whole repository to your own! And We're Only helps you to fix common Errors Not at All! 

Vegeta's Codes Based On Some Different Bots Codes One More Times Thanks to All! (for using Vegeta/for helping Vegeta)

You can find Repository to using Below link.**
"""

SOURCE_BUTTONS = [[ InlineKeyboardButton(text="Repository Link", url="https://github.com/nandhaxd/VegetaRobot")]]

@bot.on_message(filters.command(["repo","source"]))
async def repository(_, message):
        global user_id
        user_id = message.from_user.id
        await message.reply_photo(SOURCE_IMAGE,caption=SOURCE_TEXT,
        reply_markup=InlineKeyboardMarkup(SOURCE_BUTTONS))
       
CONTRIBUTORS = """
**CONTRIBUTORS**:
**Here the following list How helpful for Make Vegeta's Repository!**
[〄 ⋞ Hσdαkα ⋟ ➛](tg://user?id=5597384270)
[H ᴀ ᴄ ᴋ ᴇ ʀ ♡︎](tg://user?id=1989750989)
[🖤「 𝐋𝐨𝐯𝐞𝐥𝐲𝐏𝐫𝐢𝐧𝐜𝐞™ 」🖤 °•♡왕자♡•°](tg://user?id=5362971543)
[𝗔𝗮𝘀𝗳𝗖𝘆𝗯𝗲𝗿𝗞𝗶𝗻𝗴](tg://user?id=5446914371)
**Thanks for you all Supporting Our Bots
And We're happy to Say This!**
"""
@bot.on_callback_query(filters.regex("contributors"))
async def contributors(_, query):
      if query.from_user.id == user_id:
          await query.message.edit_caption(CONTRIBUTORS)
      else: 
          query.answer("PLZ THIS NOT YOUR REQUEST")
