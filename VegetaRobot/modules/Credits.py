import os
from pyrogram import Client, filters
from pyrogram.types import *

from VegetaRobot.conf import get_str_key
from VegetaRobot import pgram

REPO_TEXT = "[Vegeta The Robot](https://telegra.ph/file/95de573f7b0374af5375d.jpg) Powerfull group manager public Now! your going to fork this repo don't forget to give Star🌟 Don't Remove this Credits Module of VegetaRobot🙏"
  
BUTTONS = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("🤖Open bot", url=f"t.me/VegetaRobot"),
        InlineKeyboardButton("📊Network", url=f"t.me/pegasusXteam"),
      ],[
        InlineKeyboardButton("Repositorie", url="github/ctzfamily/vegetaRobot"),
      ]]
    )
  
  
@pgram.on_message(filters.command(["repo"]))
async def repo(pgram, update):
    await update.reply_text(
        text=REPO_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
