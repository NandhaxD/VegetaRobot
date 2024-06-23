

from VegetaRobot import pgram
from pyrogram import filters, types, enums, errors

import requests

from urllib.parse import quote


anime_url = "https://i.imgur.com/m5XUxTV.jpeg"

@pgram.on_message(filters.command("animeow"))
async def AnimeWatchOrder(bot, message):
       m = message
       msg = await m.reply_text("Fetching.... 🐼")
       if not len(m.text.split()) >= 2:
          return await msg.edit("Ok, read dm how to use this.")
       else:
           anime_name = quote(m.text.split(maxsplit=1)[1])
           api_url = f"https://chiaki.site/?/tools/autocomplete_series&term={anime_name}"
           try:
              response = requests.get(api_url).json()
           except Exception as e:
               return await msg.edit(
                  "❌ Error: ", str(e)
               )
           if not response:
               return await msg.edit("🐼 Sorry couldn't find the anime.")
             
           text = "✨ **Results**:\n\n" + "\n\n".join([f"✪ **{item['value']}**, {item['type']}, ﹙{item['year']}﹚" for item in response])
         
           if (await m.reply_photo(
               photo=anime_url,
               caption=text
           )):
               await msg.delete()


__mod_name__ = "Anime W-O"

__help__ = """
✨ *Anime Watch Order*:

/animeow <query>:
To Anime index to watch orderly.
"""

           
