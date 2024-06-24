import uuid
import re
from VegetaRobot import pgram, aiohttpsession as session
from aiohttp import FormData
from pyrogram import filters, types, enums, errors

def id_generator() -> str:
    return str(uuid.uuid4())

@pgram.on_message(filters.command("blackbox"))
async def blackbox(bot, message):
    m = message
    msg = await m.reply_text("Processing.....")
    
    if len(m.text.split()) == 1:
        return await msg.edit_text(
            "Type some query buddy 🐼\n"
            "/blackbox text with reply to the photo or just text"
        )
    else:
        prompt = m.text.split(maxsplit=1)[1]
        user_id = id_generator()
        image = None
        
        if m.reply_to_message and (m.reply_to_message.photo or (m.reply_to_message.sticker and not m.reply_to_message.sticker.is_video)):
            file_name = f'blackbox_{m.chat.id}.jpeg'
            file_path = await m.reply_to_message.download(file_name=file_name)
            with open(file_path, 'rb') as file:
                image = file.read()
        
        if image:
            data = FormData()
            data.add_field('fileName', file_name)
            data.add_field('userId', user_id)
            data.add_field('image', image, filename=file_name, content_type='image/jpeg')
            api_url = "https://www.blackbox.ai/api/upload"
            try:
                async with session.post(api_url, data=data) as response:
                    response_json = await response.json()
            except Exception as e:
                return await msg.edit(
                    f"❌ Error: {str(e)}"
                )
            
            messages = [
                {
                    "role": "user", 
                    "content": response_json['response'] + "\n#\n" + prompt
                }
            ]
            data = {
                "messages": messages,
                "user_id": user_id,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": {},
            }
            headers = {"Content-Type": "application/json"}
            url = "https://www.blackbox.ai/api/chat"
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    response_text = await response.text()
            except Exception as e:
                return await msg.edit(
                    f"❌ Error: {str(e)}"
                )
            
            cleaned_response_text = re.sub(r'^\$?@?\$?v=undefined-rv\d+@?\$?|\$?@?\$?v=v\d+\.\d+-rv\d+@?\$?', '', response_text)
            text = cleaned_response_text.strip()[2:]
            if "$~~~$" in text:
                text = re.sub(r'\$~~~\$.*?\$~~~\$', '', text, flags=re.DOTALL)
            rdata = {'reply': text}
        
            return await msg.edit_text(
                text=rdata['reply']
            )
        else:
            messages = [
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
            data = {
                "messages": messages,
                "user_id": user_id,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": {},
            }
            headers = {"Content-Type": "application/json"}
            url = "https://www.blackbox.ai/api/chat"
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    response_text = await response.text()
            except Exception as e:
                return await msg.edit(
                    f"❌ Error: {str(e)}"
                )
            
            cleaned_response_text = re.sub(r'^\$?@?\$?v=undefined-rv\d+@?\$?|\$?@?\$?v=v\d+\.\d+-rv\d+@?\$?', '', response_text)
            text = cleaned_response_text.strip()[2:]
            if "$~~~$" in text:
                text = re.sub(r'\$~~~\$.*?\$~~~\$', '', text, flags=re.DOTALL)
            rdata = {'reply': text}
            
            return await msg.edit_text(
                text=rdata['reply']
            )

__help__ = """
✨ *BlackBox AI*:

🌟 *Cmd*:
/blackbox: with query and reply to sticker or photo for ask
or just use it with `/blackbox what is top ten news today?`
"""

__mod_name__ = "Blackbox"
