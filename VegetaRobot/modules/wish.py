from pyrogram import filters
from VegetaRobot import pgram

@pgram.on_message(filters.command("hi"))
async def hmm(_, message):
    await message.reply_text(
        "Namaste"
    )
    
__mod_name__ = "Hi"
__help__ = """
*Hi*
- /hi: Namaste
"""
