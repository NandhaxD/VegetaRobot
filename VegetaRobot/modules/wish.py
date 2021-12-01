from pyrogram import filters
from VegetaRobot import pgram

IMG= "https://telegra.ph/file/2148458205e9f278ed12c.jpg"

@pgram.on_message(filters.command("hi"))
async def hmm(_, message):
    await message.reply_photo(IMG,caption="hi"
    )
    
__mod_name__ = "Hi"
__help__ = """
*Hi*
- /hi: Namaste
"""
