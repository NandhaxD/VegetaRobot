from bs4 import BeautifulSoup
import urllib
from VegetaRobot import telethn as tbot
from pyrogram import filters, types, enums, errors
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
from PIL import Image
from search_engine_parser import GoogleSearch

import bs4
import html2text
from bing_image_downloader import downloader
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from VegetaRobot import *
from VegetaRobot import pgram as pbot

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


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@register(pattern=r"^/reverse(?: |$)(\d*)")
async def okgoogle(img):
    """ For .reverse command, Google search images and stickers. """
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    
    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await tbot.download_media(message, photo)
    else:
        await img.reply("`Reply to photo or sticker nigger.`")
        return

    if photo:
        dev = await img.reply("`Processing...`")
        try:
            image = Image.open(photo)
        except OSError:
            await dev.edit("`Unsupported sexuality, most likely.`")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]

        if response != 400:
            await dev.edit(
                "`Image successfully uploaded to Google. Maybe.`"
                "\n`Parsing source now. Maybe.`"
            )
        else:
            await dev.edit("`Google told me to fuck off.`")
            return

        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]

        if guess and imgspage:
            await dev.edit(f"[{guess}]({fetchUrl})\n\n`Looking for this Image...`")
        else:
            await dev.edit("`Can't find this piece of shit.`")
            return

        if img.pattern_match.group(1):
            lim = img.pattern_match.group(1)
        else:
            lim = 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await tbot.send_file(
                entity=await tbot.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await dev.edit(
            f"[{guess}]({fetchUrl})\n\n[Visually similar images]({imgspage})"
        )


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""

    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "best_guess": ""}

    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    return results


async def scam(results, lim):

    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")

    imglinks = []
    counter = 0

    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        if counter < int(lim):
            imglinks.append(imglink)
        else:
            break

    return imglinks



@pbot.on_message(filters.command('enhance'))
async def enchance(_, message):
      reply = message.reply_to_message
      if not reply and (not reply.photo or reply.sticker):
            return await message.reply_text('⛔ Reply to the photo....')
      else:
           path = await reply.download(file_name=f"{message.from_user.id}.jpeg")
           msg = await message.reply_text("Wait a movement we're processing your request.")
           with open(path, 'rb') as file:
                 photo = file.read()
           encoded_image_data = base64.b64encode(photo).decode('utf-8')
           url = 'https://apis-awesome-tofu.koyeb.app/api/remini?mode=enhance'
           headers = {
                 'accept': 'image/jpg',
                 'Content-Type': 'application/json' 
           }
           data = { "imageData": encoded_image_data }
           try:
              response = requests.post(
                    url, 
                    headers=headers, 
                    json=data
              )
              await msg.edit('✨ Almost done now... sending photo... ❤️')
               
              path = 'enhanced_' + path
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
          


__mod_name__ = "Tools"

__help__ = """
 
 ❍ /img <text>*:* Search Google for images and returns them\nFor greater no. of results specify lim, For eg: `/img hello lim=10`
 ❍ /reverse: Does a reverse image search of the media which it was replie.
 
 ✪︎ /pinterest <text>: get pinterst images.
 ✪︎ /enhance: reply to the photo
 ✪︎ /ud <text>: Search for word definitions.
 ✪︎ /langs: View a list of language codes.
 ✪︎ /tr reply: Translate text messages.
 ✪︎ /share <text>: Share messages with other users.
 ✪︎ /paste reply: paste your code or text in web protocols

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
