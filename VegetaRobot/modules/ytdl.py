
from VegetaRobot import aiohttpsession as session, pgram as bot
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL

from pyrogram import filters, types, enums, errors

import io
import os

yt_music = YTMusic()




@bot.on_message(filters.command(['song', 'video']))
async def Ytdl(bot, message):
    message = message
    args = message.text.split()[1:]
    command = message.text.split()[0][1:].lower()
    if args:
        query = ' '.join(args)
        prompt = {
         'song': {'base_url': 'https://music.youtube.com/watch?v=',  'filter': 'songs', 'format': 'bestaudio[ext=m4a]'},
         'video': {'base_url': 'https://youtube.com/watch?v=', 'filter': 'videos', 'format': 'best[height<=720][ext=mp4]'}
       }
        results = yt_music.search(query, filter=prompt[command].get('filter'), limit=1)
        if not results:
            return await message.reply_text("🤷 No results for this song!")
          
        thumb_url = results[0]['thumbnails'][-1]['url']           
        msg = await message.reply_text("⚡ Downloading...")
    
        thumb_file = io.BytesIO()
        async with session.get(thumb_url) as image:
             image_content = await image.read()
             thumb_file.write(image_content)
             thumb_file.name = results[0]["videoId"] + ".jpg"
        with YoutubeDL({"format": prompt[command].get('format')}) as yt:
              info_dict = yt.extract_info(prompt[command].get('base_url') + results[0]["videoId"], download=True)
              file_path = yt.prepare_filename(info_dict)
        await msg.edit_text("⚡ Uploading...")
        
        file_msg = await (
             message.reply_audio(
                 audio=file_path,
                 quote=True,
                 title=results[0]["title"],
                 performer=results[0].get("artists", [-1])[0].get("name", None) if results[0].get("artists", []) else None,
                 thumb=thumb_file,
                 duration=results[0]["duration_seconds"]
    ) if command == 'song' else message.reply_video(
            video=file_path,
            quote=True,
            duration=results[0]["duration_seconds"],
            file_name=results[0]["title"],
            thumb=thumb_file,
    )
)
              
        if file_msg:
            await file_msg.edit_caption(
                     (
            "<b>- Downloaded successfully !\n"
            "- Title : {title}\n"
            "- Duration: {duration}\n"
            "- Is explict: {explict}\n"
            "- Message link: {link}</b>"
        ).format(
            title=results[0].get("title"),
            duration=results[0].get("duration_seconds"),
            explict=results[0].get("isExplicit"),
            link=file_msg.link
        ), 
            parse_mode=enums.ParseMode.HTML
        )
            await msg.delete()
            os.remove(file_path)     
               
    else:
       return await message.reply_text("🤷 Write some queries to find the song/video !")
