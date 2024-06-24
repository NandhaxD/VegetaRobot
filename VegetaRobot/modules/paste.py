

import os, json

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
       if response.status == 201:
            data = await response.json()
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
                'content': paste,
                'lexer': 'python',
                'expires': '604800', #expire in week
            }, headers={'Content-Type': 'application/x-www-form-urlencoded'}
        ) as response:
            if response.status != 200:
                return await msg.edit(
                   f"❌ Something went Wrong in dpaste API Status code: {str(response.status)}"
                )
            else:
              
               data = json.loads(await response.text())
               buttons = [
    [types.InlineKeyboardButton('🖥️ Paste', url=data.get('url')),
     types.InlineKeyboardButton('🖥️ Raw', url=(data.get('url') + '/raw'))]
               ]
               if shu_link:= (await shuyaa_paste(paste)):
                   buttons.append([types.InlineKeyboardButton('🐼 Paste', url=shu_link)])
               ok = await msg.reply_photo(
                photo=media_url,
      reply_markup=types.InlineKeyboardMarkup(buttons)
         )
               if ok:
                   await msg.delete()
    except Exception as e:
        return await msg.edit(f"❌ Error: {str(e)}")




__mod_name__ = "Paste"

__help__ = """
✨ *Paste*:

⚡ /paste: reply to a file or text

Start your journey to paste your codes on dpaste.com
and dev shuyaa website for share codes.
"""
