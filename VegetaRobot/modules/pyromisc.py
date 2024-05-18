import os, random , io
import requests
from PIL import Image
from pyrogram import filters
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.types import Message
from gpytranslate import Translator
from VegetaRobot import pgram as bot, pgram as app, SUPPORT_CHAT, arq
from urllib.parse import quote

       



#By @NandhaBots on telegram 

@app.on_message(filters.command("ud"))
async def urban(_, m):  
       user_id = m.from_user.id
       if len(m.text.split()) == 1:
         return await m.reply("Enter the text for which you would like to find the definition.")
       text = m.text.split(None,1)[1]
       api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
       mm = api["list"]
       if 0 == len(mm):
           return await m.reply("=> No results Found!")
       string = f"🔍 **Ward**: {mm[0].get('word')}\n\n📝 **Definition**: {mm[0].get('definition')}\n\n✏️ **Example**: {mm[0].get('example')}"
       if 1 == len(mm):
           return await m.reply(text=string, quote=True)
       else:
           num = 0
           return await m.reply(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('next', callback_data=f"udnxt:{user_id}:{text}:{num}")]]), quote=True)
              
@app.on_callback_query(filters.regex("^udnxt"))   
async def next(_, query):
         user_id = int(query.data.split(":")[1])
         text = str(query.data.split(":")[2])
         num = int(query.data.split(":")[3])+1
         if not query.from_user.id == user_id:
             return await query.answer("This is not for You!")
         api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
         mm = api["list"]
         uwu = mm[num]
         if num == len(mm)-1:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Back', callback_data=f"udbck:{query.from_user.id}:{text}:{num}")]]))
         else:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             buttons = [[
                  InlineKeyboardButton("Back ⏮️", callback_data=f"udbck:{query.from_user.id}:{text}:{num}"),
                  InlineKeyboardButton("Next ⏭️", callback_data=f"udnxt:{query.from_user.id}:{text}:{num}") 
             ]]
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^udbck"))   
async def back(_, query):
         user_id = int(query.data.split(":")[1])
         text = str(query.data.split(":")[2])
         num = int(query.data.split(":")[3])-1
         if not query.from_user.id == user_id:
             return await query.answer("This is not for You!")
         api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
         mm = api["list"]
         uwu = mm[num]
         if num == 0:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Next', callback_data=f"udnxt:{query.from_user.id}:{text}:{num}")]]))
         else:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             buttons = [[
                  InlineKeyboardButton("Back ⏮️", callback_data=f"udbck:{query.from_user.id}:{text}:{num}"),
                  InlineKeyboardButton("Next ⏭️", callback_data=f"udnxt:{query.from_user.id}:{text}:{num}") 
             ]]
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup(buttons))
       
       
       



@bot.on_message(filters.command("spell"))
async def spellcheck(_, m):
      reply = m.reply_to_message
      if not reply:
          return await m.reply_text("reply to text")
      if reply:
          x = await arq.spellcheck(reply.text)
          y = x.result
      text = await m.reply_text("Spelling...")
      await text.edit(f"`{y.corrected}`")

@bot.on_message(filters.command("wall")) 
async def wall(_, m: Message):
       if len(m.command) < 2:
           return await m.reply_text("gime a text Baka!")
       search = m.text.split(None, 1)[1]
       x = await arq.wall(search)
       y = x.result
       await m.reply_photo(random.choice(y).url_image)
       await m.reply_document(random.choice(y).url_image)

@bot.on_message(filters.command("reddit"))
async def reddit(_, m):
          if len(m.command) < 2:
              await m.reply_text("Gime text to search reddit!")
              return 
          text = m.text.split(None, 1)[1]
          x = await arq.reddit(text)
          y = x.result
          url  = y["url"]
          title = y["title"]
          await m.reply_photo(url,caption=title)

@bot.on_message(filters.command(["lang", "langs"]))
def language(_, m: Message):
       #langs codes
        m.reply_text("Click on the button below to see the list of supported language codes.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Language codes",
                        url="https://telegra.ph/Lang-Codes-03-19-3",
                    ),
                ],
            ],
        ),
    )


trans = Translator()


@bot.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Reply to a message to translate it!\n Use: /langs for translation codes")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"**Translated from {source} to {dest}**:\n"
        f"`{translation.text}`"
    )

    await message.reply_text(reply)




@bot.on_message(filters.command('json'))
async def jsonify(_, message):
    the_real_message = None
    reply_to_id = None

    if message.reply_to_message:
        the_real_message = message.reply_to_message
    else:
        the_real_message = message

    try:
        await message.reply_text(f"<code>{the_real_message}</code>")
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove("json.text")
       
       
  
def share_link(text: str) -> str:
    return "**Here is Your Sharing Text:**\nhttps://t.me/share/url?url=" + quote(text)

@bot.on_message(filters.command("share"))
async def share_text(_, message: Message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Notice:**\n\n1. Reply Any Messages.\n2. No Media Support\n\n**Any Question Join Support Chat**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Support Chat", url=f"https://t.me/vegetasupport")
                    ]                
                ]
            ),
        )
        return
    await message.reply_text(share_link(input_text))
