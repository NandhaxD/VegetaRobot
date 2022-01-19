import random

from telegram import ParseMode
from telethon import Button

from VegetaRobot import OWNER_ID, SUPPORT_CHAT
from VegetaRobot import telethn as tbot

from ..events import register


@register(pattern="/feedback ?(.*)")
async def feedback(e):
    quew = e.pattern_match.group(1)
    user_id = e.sender.id
    user_name = e.sender.first_name
    mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    VEGETA = (
        "https://telegra.ph/file/bc258c88be230d824d687.jpg",
        "https://telegra.ph/file/6ddb38a0a85a18500d49a.jpg",
        "https://telegra.ph/file/7fd1f54fc821b3f8a15a0.jpg",
        "https://telegra.ph/file/ec11e66958ccebb5f96a8.jpg",
        "https://telegra.ph/file/f5e5a31be9ba7ea30f9d0.jpg",
    )
    NATFEED = ("https://telegra.ph/file/2dd04f407b16bc2cfdf76.jpg",)
    BUTTON = [[Button.url("View Feedback ✨", f"https://t.me/{SUPPORT_CHAT}")]]
    TEXT = "Thanks For Your Feedback, I Hope You Happy With Our Service"
    GIVE = "Give Some Text For Feedback ✨"
    logger_text = f"""
**New Feedback**

**From User:** {mention}
**Username:** @{e.sender.username}
**User ID:** `{e.sender.id}`
**Feedback:** `{e.text}`
"""
    if e.sender_id != OWNER_ID and not quew:
        await e.reply(
            GIVE,
            parse_mode=ParseMode.MARKDOWN,
            buttons=BUTTON,
            file=random.choice(NATFEED),
        ),
        return

    await tbot.send_message(
        SUPPORT_CHAT,
        f"{logger_text}",
        file=random.choice(VEGETA),
        link_preview=False,
    )
    await e.reply(TEXT, file=random.choice(VEGETA), buttons=BUTTON)
