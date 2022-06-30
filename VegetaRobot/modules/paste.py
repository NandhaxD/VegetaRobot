from requests import post, get
import os
import aiofiles
import requests 
import socket
from asyncio import get_running_loop
from functools import partial
from VegetaRobot import pgram as bot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


def spacebin(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = post(url, data={"content": text, "extension": "txt"})
    return f"https://spaceb.in/{res.json()['payload']['id']}"


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()
    
async def ezup(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(
        None, partial(_netcat, "ezup.dev", 9999, content)
    )
    return link

HASTEBIN_URL = "https://www.toptal.com/developers/hastebin/documents"
HASTEBIN = "https://www.toptal.com/developers/hastebin/{}"

@bot.on_message(filters.command('paste'))
async def paste(_, m):
    reply = m.reply_to_message
    if not reply:
           wrong_format = """ **Something You did wrong read the rules of paste:**\n
        ~ Only text files or text only paste.
        ~ Text file Only support lower then 1mb.
        ~ You did Verything right but you got this msg most report on SupportChat
        """
           await m.reply_text(wrong_format)
    if reply.document:
        doc = await m.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
          file_text = await f.read()
        os.remove(doc)
        spacebin_url = spacebin(file_text)
        link = await ezup(file_text)
        caption = f"[SPACEBIN]({spacebin_url}) | [EZUP.DEV]({link})"
        await m.reply_text(text=caption,
                      reply_markup=InlineKeyboardMarkup(
                          [[InlineKeyboardButton("SPACEBIN", url=spacebin_url),
                         ],[ InlineKeyboardButton("EZUP.DEV", url=link)]]),disable_web_page_preview=True)
    elif reply.text or reply.caption:
          text = reply.text or reply.caption
          spacebin_url = spacebin(text)
          link = await ezup(text)
          key = requests.post(HASTEBIN_URL, data=text.encode("UTF-8"), ).json()
          key = key.get("key") 
          url = HASTEBIN.format(key)
          caption = f"[SPACEBIN]({spacebin_url}) | [EZUP.DEV]({link})\n         [HASTEBIN]({url})"
          await m.reply_text(text=caption,
                      reply_markup=InlineKeyboardMarkup(
                          [[InlineKeyboardButton("SPACEBIN", url=spacebin_url),
                           ],[InlineKeyboardButton("HASTEBIN", url=url),
                           ],[ InlineKeyboardButton("EZUP.DEV", url=link)]]),disable_web_page_preview=True)
    
        
        
