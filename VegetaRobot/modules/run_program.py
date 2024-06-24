import time


from pyrogram import filters, types, enums, errors
from VegetaRobot import pgram as bot, aiohttpsession as session

langs = [
  'matl', 'matl', 'bash', 'befunge93', 'bqn', 'brachylog', 'brainfuck', 'cjam', 'clojure', 
  'cobol', 'coffeescript', 'cow', 'crystal', 'dart', 'dash', 'typescript', 'javascript', 
  'basic.net', 'fsharp.net', 'csharp.net', 'fsi', 'dragon', 'elixir', 'emacs', 'emojicode',
  'erlang', 'file', 'forte', 'forth', 'freebasic', 'awk', 'c', 'c++', 'd', 'fortran', 'go', 
  'golfscript', 'groovy', 'haskell', 'husk', 'iverilog', 'japt', 'java', 'jelly', 'julia', 
  'kotlin', 'lisp', 'llvm_ir', 'lolcode', 'lua', 'csharp', 'basic', 'nasm', 'nasm64', 'nim', 
  'javascript', 'ocaml', 'octave', 'osabie', 'paradoc', 'pascal', 'perl', 'php', 'ponylang',
  'prolog', 'pure', 'powershell', 'pyth', 'python2', 'python', 'racket', 'raku', 'retina', 
  'rockstar', 'rscript', 'ruby', 'rust', 'samarium', 'scala', 'smalltalk', 'sqlite3', 'swift', 
  'typescript', 'vlang', 'vyxal', 'yeethon', 'zig'
]

api_url = 'https://nandha-api.onrender.com/run'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

@bot.on_message(filters.command('run'))
async def interpreter(bot, message):
    m = message
    
    ok = "```Example:\n/run python\n\nprint('hello world')```"
    if len(m.text.split(maxsplit=1)) >= 3:
        return await m.reply_text(text=ok)
    elif not m.text.split()[1] in langs:
         return await m.reply_text("❌ **Not A Supported language: [Click here view all available language!](https://telegra.ph/Nandha-06-24-3)**")
    code = m.text.split(maxsplit=2)[2]
    lang = m.command[1]
    data = {
        'code': code,
        'lang': lang
    }

    start_time = time.time()
    async with session.post(api_url, json=data, headers=headers) as response:
         msg = await m.reply_text("⏳ Evaluating code....")
         if response.status == 200:
              data = await response.json()
              language = data['language']
              version = data['version']
              code = data['code']
              output = data['output']
              ping = (time.time() - start_time) * 1000
              return await msg.edit_text(
f"""\n
🌐 **Language**: `{language}`
🖥️ **Version**: `{version}`

🗨️ **Code**:\n`{code}`

✨ **Result**:\n `{output}`

⚡ **Taken Time**: `{ping:.2f}'Ms`
""" )
         else:
            return await msg.edit_text("Something went wrong with the API. Please check it out 🤔")
