
import time

from VegetaRobot import pgram as bot
from pyrogram import filters


async def progress(c, t, msg, text, start):
         now = time.time()
         diff = now - start
         if round(diff % 10.00) == 0 or c == t:
               await msg.edit(f"**{text}... {c*100/t:.1f} %**")


@bot.on_message(filters.command('rename'))
async def rename(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id
      if not reply:
            return await message.reply('Reply to A file please.')
      elif not reply.media:
            return await message.reply('Reply to A file please.')        
      else:
            message_id = reply.id
        
            if not len(message.text.split()) < 2:
                 file_name = message.text.split(None, 1)[1]
            else:
                return await message.reply(
                  'Can you give filename please e.g. /rename vegeta.mkv'
                )
                
            msg = await message.reply(
                      'Downloading....'
            )
            start_dl = time.time()
              
            path = await bot.download_media(
                    message=reply,
                    file_name=file_name, 
                    progress=progress,
                    progress_args=( 
                         msg, 'Downloading', start_dl)
                )
            
            await msg.edit(
                        '**Download Complete.**'
            )
            dl_time = round(time.time()-start_dl, 2)
        
            start_ul = time.time()
            try:
                await bot.send_document(
                      chat_id=chat_id, 
                      document=path,
                      progress=progress,
                      progress_args=(msg, 'Uploading', start_ul)
            )
            except Exception as e:
                 return await msg.edit(
                   str(e)
                 )
                   
            ul_time = round(time.time()-start_ul, 2)
              
            return await msg.edit(
                    text='Download Taken Time: {}\nUpload Taken Time: {}\nThank You For Using Me. (:'.format(dl_time, ul_time)
            )
                  
