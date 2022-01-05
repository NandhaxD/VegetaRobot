import html
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from VegetaRobot.modules.disable import DisableAbleCommandHandler
from VegetaRobot import dispatcher, SUPPORT_CHAT
from requests import get
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton



@run_async
def feedback(bot: Bot, update: Update):
  name = update.effective_message.from_user.first_name
  message = update.effective_message
  userid=message.from_user.id
  text = message.text[len('/feedback '):]
   

  feed_text = f"Buddy's *New* feedback from [{name}](tg://user?id={userid})\n\nfeed: {text}"
  

  bot.sendMessage(-1001690512977, feed_text, parse_mode=ParseMode.MARKDOWN)
  

text = html.escape(text)
reply_text="Thank you for giving us your feedback."
message.reply_text(reply_text)
                                               
  

FEEDBACK_HANDLER = DisableAbleCommandHandler("feedback", feedback)

dispatcher.add_handler(FEEDBACK_HANDLER)



__help__ = """
 - /feedback : You can give us your feedbacks 
               can can see your feeds here.
"""

__mod_name__ = "FEEDBACK🗣️"


