import os
import io
import requests
import shutil 
import random
import re
import glob
import time

from io import BytesIO
from requests import get
from telethon.tl.types import InputMessagesFilterPhotos

from VegetaRobot import OWNER_ID, SUPPORT_CHAT
from VegetaRobot.events import register
from VegetaRobot import telethn
from PIL import Image, ImageDraw, ImageFont


LOGO_LINKS            = ["https://telegra.ph/file/df1331d378ea9f38a0090.jpg",
                         "https://telegra.ph/file/735c44767dda2b00442ca.jpg",
                         "https://telegra.ph/file/5503b1017a1f398090baa.jpg",
                         "https://telegra.ph/file/4e0ed6862df9f988b9f30.jpg",
                         "https://telegra.ph/file/111960e17dbae6bf20a5e.jpg",
                         "https://telegra.ph/file/f074f976a2d4a94536cf5.jpg",
                         "https://telegra.ph/file/2d7cf1d43dede0eaf1bfe.jpg",
                         "https://telegra.ph/file/f8d9b19a2d25cfd92c7fb.jpg",
                         "https://telegra.ph/file/bbf5f6ec869b3204d605c.jpg",
                         "https://telegra.ph/file/8f231b362e9c09fdf6078.jpg",
                         "https://telegra.ph/file/364185b5c141d05ad9a93.jpg",
                         "https://telegra.ph/file/722d61ca0443758dcbbfb.jpg",
                         "https://telegra.ph/file/8fe6e456525353b4c40c8.jpg",
                         "https://telegra.ph/file/73decdfd88cf8697c3953.jpg",
                         "https://telegra.ph/file/6664c32dcb5b134beb19c.jpg",
                         "https://telegra.ph/file/d3dd435d6c52fca20bb8c.jpg",
                         "https://telegra.ph/file/7647a1d211bdc1f50b82b.jpg",
                         "https://telegra.ph/file/bf1e329dee39473943939.jpg",
                         "https://telegra.ph/file/bf1ea5233b8f2759f50df.jpg",
                         "https://telegra.ph/file/c5824a10b34fedf4c2e40.jpg",
                         "https://telegra.ph/file/5652282e8c19b63e2a62a.jpg",
                         "https://telegra.ph/file/87286356a328d839df92b.jpg",
                         "https://telegra.ph/file/888f420d4dd3b168299a4.jpg",
                         "https://telegra.ph/file/02bd94586664a22b1d63f.jpg",
                         "https://telegra.ph/file/83437275bfc2b061320a3.jpg",
                         "https://telegra.ph/file/742f66b37753d48acfb4a.jpg",
                         "https://telegra.ph/file/3ff65d24bb2098e35261f.jpg",
                         "https://telegra.ph/file/f4c4b0f5ecc569a73a892.jpg",
"https://telegra.ph/file/53cf86072b5cb1d743626.jpg",
"https://telegra.ph/file/c2789ee5e396038706964.jpg",
"https://telegra.ph/file/3986db1f05132ec799ef4.jpg",
"https://telegra.ph/file/7bea67082d9bb648c4210.jpg",
"https://telegra.ph/file/a9d891dab340566de3882.jpg",
"https://telegra.ph/file/a55e21cee1dd03be2f4d3.jpg",
"https://telegra.ph/file/3f5051e8194d2a554c153.jpg",
"https://telegra.ph/file/abacfba1c4f25912fa7b3.jpg",
"https://telegra.ph/file/92baf91c90e2f784148fa.jpg"
]

@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id != OWNER_ID and not quew:
  await event.reply('**Please Gimmie A Text For The Logo**.')
  return
 pesan = await event.reply('**ᴍᴀᴋɪɴɢ ʏᴏᴜʀ ʟᴏɢᴏ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ!!!**')
 try:
    text = event.pattern_match.group(1)
    randc = random.choice(LOGO_LINKS)
    img = Image.open(io.BytesIO(requests.get(randc).content))
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./VegetaRobot/imagefiles/logofiles/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 140)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y = ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black")
    fname = "Vegeta.png"
    img.save(fname, "png")
    await telethn.send_file(event.chat_id, file=fname, caption = f"**Made by @VegetaRobot**")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'Error, Report @{SUPPORT_CHAT}, {e}')
