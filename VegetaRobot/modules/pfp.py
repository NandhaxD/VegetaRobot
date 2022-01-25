import os

from pyrogram import filters
from pyrogram.types import Message
from KURUMIBOT import pgram
from KURUMIBOT.modules.info import get_user_info

@pgram.on_message(filters.command("pfp"))
async def pfp(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) == 1:
        user = message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user = message.text.split(None, 1)[1]

    m = await message.reply_text("Processing...")

    try:
        photo_id = await get_user_info(user)
    except Exception as e:
        return await m.edit(str(e))

    if not photo_id:
        return await m.edit(
            "Please Add A Pfp In your Account", disable_web_page_preview=True
        )
    photo = await pgram.download_media(photo_id)

    await message.reply_photo(
        photo, quote=False
    )
    await m.delete()
    os.remove(photo)
