import random
import requests

from datetime import date as dt

from VegetaRobot.modules.sql.couple_sql import *
from VegetaRobot import pgram, aiohttpsession as session

from pyrogram import filters, types, enums, errors


async def GetMembers(chat_id: int):
    members = []
    async for m in pgram.get_chat_members(chat_id):
        if m.user.is_bot or m.user.is_deleted:
           continue
        members.append(m.user.id)
    return members


@pgram.on_message(filters.command(["shipping", "couples"]) & filters.group)
async def Couples(bot, m: types.Message):
    chat_id = m.chat.id
    data = {}
    today = str(dt.today())
    couple = get_couple_info(chat_id)
  
    if couple and int(couple.get('day', 0)) == int(today.split("-")[-1]):
        couple['day'] = today
        data.update(couple)  
            
    else:
        members = await GetMembers(chat_id)
        man_id, woman_id = random.sample(members, 2)
        set_couple_chat(chat_id, man_id, woman_id)
        couple = get_couple_info(chat_id)
        couple['day'] = today
        data.update(couple)

    man_id = int(data["man_id"])
    woman_id = int(data["woman_id"])
    date_str = data['day']

    try:
        info = await pgram.get_users(
          [man_id, woman_id]
        )
        man = info[0].mention
        woman = info[1].mention
      
    except Exception as e:
        man = man_id
        woman = woman_id
      
        await m.reply_text(f"❌ Error when getting info: {str(e)}")

    
  
    photo_url = "https://graph.org/file/0e36d05c9e5fe01d3b986.jpg"
    try:
      api_url = "https://nandha-api.onrender.com/couples"
      async with session.get(api_url) as resp:
           status = resp.status
           if status == 200:
                data = await resp.json()
                man_image = data['male_image']
                woman_image = data['female_image']
                await pgram.send_media_group(
                    chat_id, 
                     media=([
              types.InputMediaPhoto(man_image),
              types.InputMediaPhoto(woman_image)
          ])) 
           else:
              await m.reply_text(
                 "❌ Error while Fetching couples pfp Status code:", str(status)
              )
                                
    except Exception as e:
        await m.reply_text(
           "❌ Error occured while fetching a couples pfp:", str(e)
        )
  
    string = (
        f"""
💍🎉 𝐍𝐞𝐰𝐥𝐲𝐰𝐞𝐝𝐬 𝐂𝐨𝐮𝐩𝐥𝐞 🎉💍

📅 𝐃𝐚𝐲: **{date_str}**
🤵 𝐌𝐚𝐧: **{man}**
👰 𝐖𝐨𝐦𝐚𝐧: **{woman}**

💖 **Wishing you a lifetime of love and happiness! by {bot.me.mention}** 💖
"""
    )
    await m.reply_photo(
      photo=photo_url,
      caption=string
    )
