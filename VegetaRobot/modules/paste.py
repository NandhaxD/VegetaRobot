

import os
from requests import get, post
from requests.exceptions import HTTPError, Timeout, TooManyRedirects

from VegetaRobot import pgram

from pyrogram import filters, types, enums, errors


media_url = "https://graph.org/file/cb336f4cc339dbbd5b5d3.jpg"

@pgram.on_message(filters.command('paste'))
async def dpaste(bot, message):
    m = message
    reply = message.reply_to_message
    api_url = "https://dpaste.org/api/"

    msg = await m.reply_text("✨ Please patience....")
    if reply and reply.text:
         paste = reply.text
    elif reply and reply.document and reply.document.mime_type.startswith('text/'):
         await msg.edit("✨ File downloading...")
         file = await reply.download()
         with open(file, 'r') as f:
             paste = f.read()
         os.remove(file)
    else:
        return await msg.edit_text(
          "Reply to the message text or file text"
        )

    await msg.edit("🐼 Pasting...")
    try:
        r = post(
            url=api_url,
            data={
                'format': 'default',
                'content': paste.encode('utf-8'),
                'lexer': 'python',
                'expires': '604800', #expire in week
            },
        )
    except Exception as e:
        return await msg.edit("❌ Error:", str(e))
    ok = await msg.reply_photo(
      photo=media_url,
      reply_markup=types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton('🖥️ Paste Link', url=str(r.text))
      ],[
        types.InlineKeyboardButton('🖥️ Raw Link', url=(str(r.text)+'/raw'))
      ]])
    )
    if ok:
       await msg.delete()
