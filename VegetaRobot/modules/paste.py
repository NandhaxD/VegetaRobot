

import os
from requests import get, post
from requests.exceptions import HTTPError, Timeout, TooManyRedirects

from VegetaRobot import pgram

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
                'format': 'url',
                'content': paste.encode('utf-8'),
                'lexer': 'python',
                'expires': '604800', #expire in week
            },
        )
    except Exception as e:
        await msg.edit("❌ Error:", str(e))
    await msg.edit(
      "✨ Paste Link: ", r.text
    )
    
