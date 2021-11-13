import os
from pyrogram import Client, filters
from pyrogram.types import *

from VegetaRobot.conf import get_str_key
from VegetaRobot import pgram

REPO_TEXT = "[Vegeta The Robot](https://telegra.ph/file/95de573f7b0374af5375d.jpg) \nPowerfull group manager public Now! \nyour going to fork this repo don't forget to give Star🌟 Don't Remove this Credits Module 🙏"
  
BUTTONS = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("Open bot", url=f"https://t.me/vegetaRobot"),
        InlineKeyboardButton("Network", url=f"https://t.me/pegasusXteam"),
      ],[
        InlineKeyboardButton("Repositorie", url="https://github.com/ctzfamily/vegetaRobot"),
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
