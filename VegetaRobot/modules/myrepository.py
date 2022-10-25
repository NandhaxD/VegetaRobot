from VegetaRobot import pgram, aiohttpsession as session
from pyrogram import filters
from pyrogram.types import *



async def get(url: str, *args, **kwargs):
    async with session.get(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data

@pgram.on_message(filters.command("repo",config.CMDS))
async def repo(_, m):
    chat_id = message.chat.id
    users = await get("https://api.github.com/repos/NandhaxD/VegetaRobot/contributors")
    list_of_users = ""
    count = 1
    for user in users:
        list_of_users += (f"**{count}.** [{user['login']}]({user['html_url']})\n")
        count += 1
        total = count-1
    text = f"""
[ `Contributors in Vegeta` ]

{list_of_users}
[`Contributors: {total}`]"""
    await pgram.send_message(chat_id,text=text,
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Repo",url="https://gitHub.com/NandhaxD/VegetaRobot"),
InlineKeyboardButton("Group",url="t.me/VegetaSupport"),]]) ,reply_to_message_id=message.id ,disable_web_page_preview=True)
