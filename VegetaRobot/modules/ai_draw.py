

import random

from VegetaRobot import pgram, aiohttpsession as session, BOT_USERNAME
from pyrogram import filters, types, enums, errors



@pgram.on_message(filters.command('draw'))
async def Draw(bot, message): # Hey kagger (:
    m = message
    if len(m.text.split()) < 2:
        return await m.reply_text("🙋 where prompt ?")
    url=f"https://image.pollinations.ai/prompt/{m.text.split(maxsplit=1)[1]}{random.randint(1, 10000)}"
    async with session.get(url) as response:
        image = await response.read()
        await m.reply_photo(
          image, caption="**💀 By @{bot.me.username}**"
      )
         


__mod_name__ = "Draw"

__help__ = f"""
✨ **AI DRAW**:

Text to Image System by @{BOT_USERNAME}
Use `/draw anime cute girl`
"""

