from bs4 import BeautifulSoup
import urllib
import glob
import io
import os
import re
import base64
import aiohttp
import urllib.request
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from telegraph import upload_file
from PIL import Image

import bs4
import html2text

from bing_image_downloader import downloader
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram import filters, types, enums, errors


from urllib.parse import quote_plus
from unidecode import unidecode
from VegetaRobot import *
from VegetaRobot import pgram as pbot
from VegetaRobot import pgram as app
from VegetaRobot import telethn as tbot
from VegetaRobot.events import register


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern="^/img (.*)")
async def img_sampler(event):
    if event.fwd_from:
        return
    
    query = event.pattern_match.group(1)
    jit = f'"{query}"'
    downloader.download(
        jit,
        limit=4,
        output_dir="store",
        adult_filter_off=False,
        force_replace=False,
        timeout=60,
    )
    os.chdir(f'./store/"{query}"')
    types = ("*.png", "*.jpeg", "*.jpg")  # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    await tbot.send_file(event.chat_id, files_grabbed, reply_to=event.id)
    os.chdir("/app")
    os.system("rm -rf store")



class GoogleReverseImageSearch:
    """
    A class for performing a reverse image search on Google.
    """

    GOOGLE_IMAGE_SEARCH_URL = "https://images.google.com/searchbyimage?safe=off&sbisrc=tg&client=app&image_url={img_url}"
    USER_AGENT = (
        "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 "
        "Mobile Safari/537.36"
    )

    def __init__(self) -> None:
        """
        Initialize the GoogleReverseImageSearch instance.
        """
        self._client = requests.Session()

    @staticmethod
    def _get_image_url(address: str):
        """
        Get the image URL, either from a file upload or directly if it's a URL.

        Returns:
            str: The image URL.
        """
        if os.path.isfile(address):
            assert (
                os.path.getsize(address) <= 5979648
            ), "File size must be less than 5.7 MB"
            return f"https://graph.org{upload_file(address)[0]}"
        else:
            return address

    def reverse_search_image(self, address: str):
        """
        Perform a reverse image search on Google and retrieve results.

        Returns:
            dict: A dictionary containing search results, including 'similar' and 'output'.
        """
        img_url = self._get_image_url(address=address)
        response = self._client.get(
            url=self.GOOGLE_IMAGE_SEARCH_URL.format(img_url=img_url),
            headers={"User-agent": self.USER_AGENT},
        )
        soup = BeautifulSoup(response.text, "html.parser")
        result = {"similar": response.url, "output": ""}
        for best in soup.find_all("div", {"class": "r5a77d"}):
            output = best.get_text()
            result["output"] = unidecode(output)

        return result




async def get_file_id_from_message(msg):
    file_id = None
    message = msg.reply_to_message
    if not message:
        return
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id

@app.on_message(filters.command(["pp", "grs", "reverse", "r"]))
async def _reverse(_, msg):

    user_id = msg.from_user.id
    
    text = await msg.reply("**⏫ Uploading To Google Search Engine**")
    file_id = await get_file_id_from_message(msg)
    try:
        if not file_id:
             return await text.edit("`Dear Pro People's Please Reply To A Media File 🗃️`")
    
        await text.edit("**🌐 Wait For >1 Min Searching Your Prompt**")

        path = f"reverse_{user_id}.jpeg"
        image = await app.download_media(
           message=file_id, file_name=path
    )
    
        grap = upload_file(image)
        for code in grap:
              grap_url = "https://graph.org"+code

        google = GoogleReverseImageSearch()
        result = google.reverse_search_image(address=grap_url)

      
        if not result.get("output", None):
            return await text.edit("**❌ No result found for this.**")

        button = reply_markup=types.InlineKeyboardMarkup([[
          types.InlineKeyboardButton('Similar ✨', url=result["similar"]),
          types.InlineKeyboardButton('Telegrap ✨', url=grap_url)
          
        ]])
        reply_text = (
            
          f'**🔍 Google**: {result["output"]}\n\n'
          f'**Made by @VegetaRobot**'
            
        )


        await text.edit_text(
          text=reply_text, reply_markup=button, parse_mode=enums.ParseMode.MARKDOWN)
      
   
    except Exception as e:
        await text.edit(f"❌ Error occured: {e}")
        



@pbot.on_message(filters.command('enhance'))
async def enchance(_, message):
      reply = message.reply_to_message
      user_id = message.from_user.id
  
      if not reply and (not reply.photo or not reply.sticker):
            return await message.reply_text('⛔ Reply to the photo....')
      else:
           path = await reply.download(
             file_name=f"{user_id}.jpeg"
           )
        
           msg = await message.reply_text("Wait a movement we're processing your request.")
           with open(path, 'rb') as file:
                 photo = file.read()
             
           encoded_image_data = base64.b64encode(photo).decode('utf-8')
        
           url = 'https://apis-awesome-tofu.koyeb.app/api/remini?mode=enhance'
           headers = {
                 'accept': 'image/jpg',
                 'Content-Type': 'application/json' 
           }
           data = {
             "imageData": encoded_image_data 
           }
        
           try:
              response = requests.post(
                    url, 
                    headers=headers, 
                    json=data
              )
              await msg.edit(
                '✨ Almost done now... Sending photo... ❤️'
              )
               
              path = f"enhanced_{user_id}.jpeg"
             
              with open(path, 'wb') as file:
                  file.write(response.content)
              
              if (await message.reply_document(
                   document=path, quote=True
              )):
                   await msg.delete()
                  
              
           except Exception as e:
                return await message.reply_text(
                    f"❌ Error occurred when processing: `{e}`"
                )
           
                     


# by aditiya
@pbot.on_message(filters.command(["pinterest","pintst"]))
async def pinterest(_, message):
     chat_id = message.chat.id
     try:
       query= message.text.split(None,1)[1]
     except:
         return await message.reply("Input image name for search 🔍")
         
     images = requests.get(f"https://pinterest-api-one.vercel.app/?q={query}").json()

     media_group = []
     count = 0

     msg = await message.reply(f"scaping images from pinterest...")

     for url in images["images"][:6]:
                  
          media_group.append(types.InputMediaPhoto(url))
          count += 1
          await msg.edit(f"=> ✅ Scaped {count}")

     try:
        
        await pbot.send_media_group(
                chat_id=chat_id, 
                media=media_group,
                reply_to_message_id=message.id)
        return await msg.delete()

     except Exception as e:
           await msg.delete()
           return await message.reply(f"Error\n{e}")
          


def webss(url: str, user_id: int):
      payload = {
         "url": url,
         "width": 1920,
         "height": 1080,
         "scale": 1,
         "full": True,
         "format": "jpeg"}
      response = requests.post("https://webscreenshot.vercel.app/api", data=payload)
      data = response.json()
      b = data["image"].replace("data:image/jpeg;base64,", "")
      file = io.BytesIO(base64.b64decode(b))
      path = f'webss_{user_id}.jpeg'
      with open(path, 'wb') as f:
           f.write(file.getbuffer())
      return path

  


@pbot.on_message(filters.command('webss'))
async def take_ss(_, message):
     regex = r"\b(?:https?|ftp):\/\/[-A-Za-z0-9+&@#\/%?=~_|!:,.;]*[-A-Za-z0-9+&@#\/%=~_|]"
    
     if not len(message.command) == 2:
          return await message.reply_text(
              "WELL, WELL, where is the url ??"
          )
      
     text = ' '.join(message.command[1:])
     matches = re.findall(regex, text)
  
     msg = await message.reply_text("Wait a movement we're processing your request. ✨")
     if len(matches) > 0:
          url = matches[0]
          try:
            document = webss(
              url, message.from_user.id
            )
            if (await message.reply_document(
         document=document, quote=True)):
                 await msg.delete()
          except Exception as e:
               return await msg.edit_text(
                   f"❌ Error occurred: {e}"
               )
     else:
         return await message.reply_text(
             "No url detected in text 💀"
         )
          
    







__mod_name__ = "Tools"

__help__ = """
 
 ❍ /img <text>*:* Search Google for images and returns them\nFor greater no. of results specify lim, For eg: `/img hello lim=10`
 ❍ /reverse: Does a reverse image search of the media which it was replie.
 
 ✪︎ /pinterest <text>: get pinterst images.
 ✪︎ /enhance: reply to the photo
 ✪︎ /webss: take screenshot from website.
 ✪︎ /ud <text>: Search for word definitions.
 ✪︎ /langs: View a list of language codes.
 ✪︎ /tr reply: Translate text messages.
 ✪︎ /share <text>: Share messages with other users.
 ✪︎ /paste reply: paste your code or text in web protocols
 ✪︎ /carbon: reply to the message text

*Zip a files And Unzip files*
 ❍ /zip: reply to a telegram file to compress it in .zip format
 ❍ /unzip: reply to a telegram file to decompress it from the .zip format.
 
 *hide a text and show hide a text*
 ❍ /hide - reply to (text) hide a text.
 ❍ /show - reply to hide (text) showing hide text to normal text.
  
*Telegraph Uploader only upload 3 to 5 mb files*
 ❍ /tm: upload image or GIFs telegraph.
 ❍ /txt: reply to text, text upload in telegraph.
"""
