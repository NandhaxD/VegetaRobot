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

        data = response.json()
        media_list = data.get("result", [])

        if url.startswith("https://www.instagram.com/p/"):
            media_group = []
            for media_url in media_list[:8]:
                media_group.append(InputMediaPhoto(media=media_url))

            lalal = await message.reply(f"=> Fetched {len(media_group)} Media")
            await pbot.send_media_group(chat_id=chat_id, media=media_group)
            await lalal.delete()

        elif url.startswith("https://www.instagram.com/reel/"):
            for video_url in media_list:
                await pbot.send_video(chat_id=chat_id, video=video_url)

        elif url.startswith("https://www.instagram.com/stories/"):
            for story_url in media_list:
                try:
                    await pbot.send_video(chat_id=chat_id, video=story_url)
                    await asyncio.sleep(0.3)
                except Exception as e:
                    await message.reply(f"Error sending video: {e}")

        else:
            await message.reply("Invalid Instagram link")

    except Exception as e:
        await message.reply(f"Error: {e}")
