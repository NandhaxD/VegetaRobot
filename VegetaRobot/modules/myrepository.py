
import requests 

from VegetaRobot import pgram, aiohttpsession as session
from pyrogram import filters
from pyrogram.types import *




@pgram.on_message(filters.command("noise"))
async def repo(_, m):
    chat_id = m.chat.id
    users = requests.get("t.me/CyberPunk_25").json()
    list_of_users = ""
    count = 1
    for user in users:
        list_of_users += (f"**{count}.** [{user['login']}]({user['html_url']})\n")
        count += 1
        total = count-1
    text = f"""
[ Contact @CyberPunk_25 ]

{list_of_users}
[`Contributors: {total}`]"""
    await pgram.send_message(chat_id,text=text,
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Repo",url="t.me/CyberPunk_25"),
InlineKeyboardButton("Group",url="t.me/MissRubiSupport"),]]) ,reply_to_message_id=m.id ,disable_web_page_preview=True)
