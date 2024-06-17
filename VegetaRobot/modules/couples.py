import random
from datetime import date as dt

from VegetaRobot.modules.sql.couple_sql import *
from VegetaRobot import pgram

from pyrogram import filters, types, enums, errors


async def GetMembers(chat_id: int):
    members = []
    async for m in pgram.get_chat_members(chat_id):
        members.append(m.user.id)
    return members


@pgram.on_message(filters.command(["shipping", "couples"]) & filters.group)
async def Couples(bot, m: types.Message):
    chat_id = m.chat.id
    is_couple = is_couple_chat(chat_id)
    data = None
    today = str(dt.today())
    couple = get_couple_info(chat_id)
  
    if is_couple and (couple.get('day', 0) == int(today.split("-")[-1])):
        couple['day'] = today
        data = couple    
            
    else:
        members = await GetMembers(chat_id)
        man_id, woman_id = random.sample(members, 2)
        set_couple_chat(chat_id, man_id, woman_id)
        couple['day'] = today
        data = couple

    man_id = data["man_id"]
    woman_id = data["woman_id"]
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
      caption=string)
