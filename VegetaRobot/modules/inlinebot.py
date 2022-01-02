
import socket
import json
import sys
from time import time
import aiohttp
from aiohttp import ClientSession
from motor import version as mongover
from pykeyboard import InlineKeyboard
from pyrogram import __version__ as pyrover

from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)

from VegetaRobot import pgram

async def alive_function(answers):
    buttons = InlineKeyboard(row_width=2)
    bot_state = "Dead" if not await app.get_me() else "Alive"
    # ubot_state = 'Dead' if not await app2.get_me() else 'Alive'
    buttons.add(
        InlineKeyboardButton("🔐 Main Bot", url="https://t.me/ZeusXRobot?start=help"),
        InlineKeyboardButton("🔄 Go Inline", switch_inline_query_current_chat=""),
    )

    msg = f"""
**[Zeus 🖤](https://github.com/Ctzfamily/VegetaRobot):**
**MainBot:** `{bot_state}`
**UserBot:** `Alive`
**Python:** `3.9`
**Pyrogram:** `{pyrover}`
**Platform:** `{sys.platform}`
**Profiles:** [BOT](t.me/VegetaRobot) | [REPO](https://github.com/Ctzfamily/VegetaRobot)
"""
    answers.append(
        InlineQueryResultArticle(
            title="Alive",
            description="Check Bot's Stats",
            thumb_url="https://telegra.ph/file/93203499260184ff876b5.jpg",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=buttons))

@pgram.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.lower()
        answers = []
        if text.split()[0] == "alive":
            answerss = await alive_function(answers)
            await client.answer_inline_query(query.id, results=answerss, cache_time=10))

        
