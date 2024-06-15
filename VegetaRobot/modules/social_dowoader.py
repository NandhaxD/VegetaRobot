from VegetaRobot import pgram
from pyrogram import filters, types, enums, errors
import re
import requests
import bs4


def is_instagram_url(text: str) -> bool:
    pattern = r'^https://www\.instagram\.com*'
    return bool(re.match(pattern, text))

api_url = "https://v3.saveig.app/api/ajaxSearch"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*"
}

@pgram.on_message(filters.command(['instadl', 'igdl', 'instagramdl']))
async def Instagram_download(bot, message):
    m = message
    if len(message.text.split(maxsplit=1)) != 2:
        return await m.reply_text("**Can you provide me the url please 👀**")
    url = message.text.split(maxsplit=1)[1]
    msg = await m.reply_text("Fetching data please wait 🔍")
    Instagram = is_instagram_url(url)
    if not Instagram:
        return await msg.edit_text(
            "🤔 Please give only Instagram url!\n```Example\n/instadl https://www.instagram.com/p/C4RmRkRPZ6w/?igsh=MXNwbHhkNjFiZWN3YQ==```"
        )
    else:
        data = {
            "q": url,
            "t": "media",
            "lang": "en"
        }
        response = requests.post(api_url, headers=headers, data=data)
        if response.status_code != 200:
            return await msg.edit_text("❌ Error while Fetching data...")
        else:
            response_json = response.json()
            if 'data' in response_json:
                html_content = response_json['data']
                soup = bs4.BeautifulSoup(html_content, 'html.parser')
                download_div = soup.find('div', class_='download-items__btn')
                download_btn = download_div.find('a') if download_div else None
                if download_btn:
                    video_url = download_btn['href']
                    return await bot.send_document(
                        chat_id=m.chat.id, 
                        document=video_url, 
                        reply_to_message_id=m.id,
                        force_document=False
                    )
                else:
                    return await msg.edit("No media found 👀")
            else:
                return await msg.edit("No data found for media ❌")
