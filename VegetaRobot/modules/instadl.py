from requests import get 
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from VegetaRobot import pgram as pbot, SUPPORT_CHAT
import asyncio

"""
Credits
t.me/SIAmKira
t.me/HoshinoXUpdates
https://hoshi-api-f62i.onrender.com/
"""





@pbot.on_message(filters.command(["insta","ig", "instadl"]))
async def insta_download(client, message):
    try:
        url = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Provide URL. Usage: /insta [url]")

    
    chat_id = message.chat.id

    try:
        response = get(f"https://hoshi-api-f62i.onrender.com/api/insta?url={url}")
        if response.status_code != 200:
            return await message.reply(f"Error fetching Instagram data. Status code: {response.status_code}\nReport @{SUPPORT_CHAT}")

        msg = await message.reply_text(
        text="🔍 Fetching media's please wait...."
        )
      
        data = response.json()
        media_list = data.get("result", [])

        if url.startswith("https://www.instagram.com/p/"):
            media_group = []
            for media_url in media_list[:8]:
                media_group.append(
                  InputMediaPhoto(media=media_url)
                )

            await msg.edit_text(f"⚡ Successfully Fetched {len(media_group)} Media")
            ok = await pbot.send_media_group(
              chat_id=chat_id, 
              media=media_group
            )
            if ok: return await msg.delete()

        elif url.startswith("https://www.instagram.com/reel/"):
            for video_url in media_list:
                ok = await pbot.send_video(
                  chat_id=chat_id,
                  video=video_url
                )
                if ok: return await msg.delete()

        elif url.startswith("https://www.instagram.com/stories/"):
            await msg.edit("Uploading stories ⚡")
            for story_url in media_list:
                try:
                    await pbot.send_video(chat_id=chat_id, video=story_url)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    await message.reply_text(f"{story_url}: Error sending video: {e}")
            await msg.delete()
        else:
            await msg.edit_text("Invalid Instagram link")

    except Exception as e:
        await msg.edit(f"Error: {e}")
