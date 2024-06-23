
import uuid
import re
import requests

from VegetaRobot import pgram
from pyrogram import filters, types, enums, errors



def IdGenerator() -> str:
    return uuid.uuid4()

@pgram.on_message(filters.command("blackbox"))
async def blackbox(bot, message):
      m = message
      if len(m.text.split()) == 1:
          return await m.reply_text(
             "type some query buddy 🐼\n"
             "/blackbox text with reply to the photo or just text"
          )
       else:
           prompt = m.text.split(maxsplit=1)[1]
           user_id = IdGenerator()
           image = None
           
           if m.reply_to_message and m.reply_to_message.photo:
                 file_name = f'blackbox_{m.chat.id}.jpeg'
                 file_path = await m.reply_to_message.download(file_name=file_name)
                 with open(file_path, 'rb') as file:
                      image = file.read()
           if image:
                files = {'image': (file_name, image, 'image/jpeg')}
                data = {'fileName': file_name, 'userId': user_id}
                api_url = "https://www.blackbox.ai/api/upload"
                response = requests.post(api_url, files=files, data=data)
                response_json = response.json()
                messages = [{"role": "user", "content": response_json['response'] + "\n#\n" + prompt}]
                data = {
                "messages": messages,
                "user_id": user_id,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": {},
                }
                headers = {"Content-Type": "application/json"}
                url = "https://www.blackbox.ai/api/chat"
                response = requests.post(url, headers=headers, json=data)
                cleaned_response_text = re.sub(r'^\$?@?\$?v=undefined-rv\d+@?\$?|\$?@?\$?v=v\d+\.\d+-rv\d+@?\$?', '', response_text)
                text = cleaned_response_text.strip()[2:]
                if "$~~~$" in text:
                    text = re.sub(r'\$~~~\$.*?\$~~~\$', '', text, flags=re.DOTALL)
                rdata = {'reply': text}
                return await m.reply_text(
                      text=rdata['reply']
             )


                
                










