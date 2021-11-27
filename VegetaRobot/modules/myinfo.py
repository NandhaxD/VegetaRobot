from telethon import events, Button, custom, version
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import os,re
import requests
import datetime
import time
from datetime import datetime
import random
from PIL import Image
from io import BytesIO
from VegetaRobot import telethn as bot
from VegetaRobot import telethn as tgbot
from VegetaRobot.events import register
from VegetaRobot import dispatcher


edit_time = 5
""" =======================VEGETA====================== """
file1 = "https://telegra.ph/file/bc258c88be230d824d687.jpg"
file2 = "https://telegra.ph/file/6ddb38a0a85a18500d49a.jpg"
file3 = "https://telegra.ph/file/7fd1f54fc821b3f8a15a0.jpg"
file4 = "https://telegra.ph/file/ec11e66958ccebb5f96a8.jpg"
file5 = "https://telegra.ph/file/f5e5a31be9ba7ea30f9d0.jpg"
""" =======================VEGETA====================== """


@register(pattern="/myinfo")
async def proboyx(event):
    chat = await event.get_chat()
    current_time = datetime.utcnow()
    firstname = event.sender.first_name
    button = [[custom.Button.inline("information",data="information")]]
    on = await bot.send_file(event.chat_id, file=file2,caption= f"hello {firstname}, \n Click The Button Below To Get Your Info", buttons=button)

    await asyncio.sleep(edit_time)
    ok = await bot.edit_message(event.chat_id, on, file=file3, buttons=button) 

    await asyncio.sleep(edit_time)
    ok2 = await bot.edit_message(event.chat_id, ok, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok3 = await bot.edit_message(event.chat_id, ok2, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok4 = await bot.edit_message(event.chat_id, ok3, file=file2, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok5 = await bot.edit_message(event.chat_id, ok4, file=file1, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok6 = await bot.edit_message(event.chat_id, ok5, file=file3, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
  try:
    boy = event.sender_id
    PRO = await bot.get_entity(boy)
    LILIE = "POWERED BY UNITED \n\n"
    LILIE += f"FIRST NAME : {PRO.first_name} \n"
    LILIE += f"LAST NAME : {PRO.last_name}\n"
    LILIE += f"YOU BOT : {PRO.bot} \n"
    LILIE += f"RESTRICTED : {PRO.restricted} \n"
    LILIE += f"USER ID : {boy}\n"
    LILIE += f"USERNAME : {PRO.username}\n"
    await event.answer(LILIE, alert=True)
  except Exception as e:
    await event.reply(f"{e}")

__help__ = """
/myinfo: shows your info in inline button
"""

__mod_name__ = "📓MYINFO"
__command_list__ = [
    "myinfo"
]


#myinfo module by Valt
#Copyright by @pegasusXteam

