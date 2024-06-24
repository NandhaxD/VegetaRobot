

import os

from VegetaRobot import pgram, aiohttpsession as session
from pyrogram import filters, types, enums, errors


async def shuyaa_paste(text: str):
    base_url = "https://snippetsbin.vercel.app/"
    api_url = "https://snippetsbin.vercel.app/api/snippets"
    payload = {
       'code': text,
       'language': 'python',
       'expireTime': '120' # auto delete after 2 hours
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    async with session.post(
         api_url,
         json=payload,
         headers=headers
    ) as response:
       if response.status == 200:
            data = response.json()
            return base_url + data['uniqueCode']
       else:
            return None


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
        async with session.post(
            url=api_url,
            data={
                'format': 'json',
                'content': paste.encode('utf-8'),
                'lexer': 'python',
                'expires': '604800', #expire in week
            },
        ) as response:
            if response.status != 200:
                return await msg.edit(
                   "Something went wrong Status code:", str(response.status)
                )
            else:
              
               data = response.json()
               buttons = [
    [types.InlineKeyboardButton('🖥️ Paste', url=data.get('url')),
     types.InlineKeyboardButton('🖥️ Raw', url=(data.get('url') + '/raw'))]
               ]
               if shu_link:= (await shuyaa_paste(paste)):
                   buttons.append([types.InlineKeyboardButton('🐼 Paste', url=shu_link)])
               ok = await msg.reply_photo(
                photo=media_url,
      reply_markup=types.InlineKeyboardMarkup([])
         )
               if ok:
                   await msg.delete()
    except Exception as e:
        return await msg.edit("❌ Error:", str(e))
    
