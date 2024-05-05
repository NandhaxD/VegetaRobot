
from VegetaRobot import pgram as bot
from pyrogram import filters, types


import requests


SUPPORT_CHAT = -1002114500517
repo_name = 'VegetaRobot'
repo_owner = 'NandhaxD'

commit_ids = []

api = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'


String = (
  '**Author**: {}\n'
  '**Committer**: {}\n'
  '**Email**: {}\n'
  '**Date**: {}\n\n'
  '**Message**:\n{}'
)

@bot.on_message(filters.chat(SUPPORT_CHAT) & ~filters.bot, group=3)
async def notify_commit(_, message):
      if len(commit_ids) == 0:
           rsp = requests.get(api).json()
           commit_id = rsp[0]['commit']['url'].split('/')[-1]
           author = rsp[0]['commit']['author']['name']
           name = rsp[0]['commit']['committer']['name']
           url = rsp[0]['commit']['url']
           email = rsp[0]['commit']['committer']['email']
           msg = rsp[0]['commit']['message']
           date = rsp[0]['commit']['committer']['date']
           button = [[types.InlineKeyboardButton(text='Vist Commit 👀', url=url)]]
           await bot.send_message(
                    chat_id=SUPPORT_CHAT,
                    text=String.format(author, name, email, date, msg),
                    reply_markup=types.InlineKeyboardMarkup(button))
           commit_ids.append(commit_id)
      else:
          if len(commit_ids) != 0:
              Scommit_id = commit_ids[0]
              rsp = requests.get(api).json()
              commit_id = rsp[0]['commit']['url'].split('/')[-1]
              if Scommit_id != commit_id:
                  author = rsp[0]['commit']['author']['name']
                  name = rsp[0]['commit']['committer']['name']
                  url = rsp[0]['commit']['url']
                  email = rsp[0]['commit']['committer']['email']
                  msg = rsp[0]['commit']['message']
                  date = rsp[0]['commit']['committer']['date']
                  commit_ids.clear()
                  await bot.send_message(
                    chat_id=SUPPORT_CHAT,
                    text=String.format(author, name, email, date, msg),
                    reply_markup=types.InlineKeyboardMarkup(button))
                  commit_ids.append(commit_id)



