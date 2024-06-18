
import re, os
from pytube import YouTube


from pyrogram import filters, types, enums, errors
from VegetaRobot import pgram


pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\w{11})|(?:youtu\.be\/\w{11}))(?:\S+)?'


def is_youtube_url(text: str):
    match = re.search(pattern, text)
    url = None
    if match:
        url = match.group(0)
    return url



def download(link: str, mode: str):
    yt = YouTube(link)
    if mode == "ytaudio":
        file = yt.streams.get_audio_only()
        path = file.download('./')
        new_file_path = os.path.splitext(path)[0] + ".mp3"      
        os.rename(path, new_file_path)
    else:
        file = yt.streams.get_highest_resolution()
        path = file.download('./')
    return [ yt.title, path ]



@pgram.on_message(filters.command(['ytaudio','ytvideo']))
async def youtube_dl(bot, m: types.Message):
       cmd = m.command[0]
       if not len(m.text.split()) >= 2:
            return await m.reply_text("```Example:\n/ytvideo url```")
       else:
          link = is_youtube_url(m.text)
          if not link:
              return await m.reply_text("🤔 not youtube link")
          else:
              msg = await m.reply_text("✨ Downloading....")
              try:
                 title, path = download(link, cmd)
              except Exception as e:
                  return await msg.edit(f"❌ Error: {e}")
              if (await m.reply_document(
                   document=path, caption=title, force_document=False, quote=True
              )):
                   await msg.delete()
                  
             
        


