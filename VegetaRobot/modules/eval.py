import io
import os
import sys
import time
import requests as req
import pyrogram

from pyrogram import filters, types, enums, errors

# Common imports for eval
import textwrap
import traceback
from contextlib import redirect_stdout
from telethon.sync import events

from VegetaRobot import LOGGER, dispatcher, pgram as pbot, OWNER_ID
from VegetaRobot import telethn as client, DEV_USERS
from VegetaRobot.modules.helper_funcs.chat_status import dev_plus
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, run_async

namespaces = {}

thumb = "./VegetaRobot/resources/IMG_20211227_141907_345.jpg"

async def pyroaexec(code, pbot, message, my, m, r, ru):
    exec(
        "async def __pyroaexec(pbot, message, my, m, r, ru): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__pyroaexec"](pbot, message, my, m, r, ru)


 
def p(*args, **kwargs):
    print(*args, **kwargs)
	

@pbot.on_message(filters.command('peval') & filters.user(DEV_USERS))
async def pyroevaluate(pbot, message):
    
    status_message = await message.reply("`Running Code...`")
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    start_time = time.time()

    r = message.reply_to_message	
    m = message
    my = getattr(message, 'from_user', None)
    ru = getattr(r, 'from_user', None)

    if r:
        reply_to_id = r.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await pyroaexec(
		code=cmd, 
		message=message,
		my=my,
		m=message, 
		r=r,
		ru=ru,
		pbot=pbot
	)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    taken_time = round((time.time() - start_time), 3)
    output = evaluation.strip()
    format_text = "<pre>Command:</pre><pre language='python'>{}</pre> \n<pre>Takem Time: {}'s:</pre><pre language='python'> {}</pre>"
    final_output = format_text.format(cmd, taken_time, output)
	
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            thumb=thumb,
            caption=f'`{cmd}`',
            quote=True,
            
        )
        os.remove(filename)
        await status_message.delete()
        return
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.HTML)
        return 



def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            '__builtins__': globals()['__builtins__'],
            'bot': bot,
	    'reply': update.effective_message.reply_to_message,
            'message': update.effective_message,
            'user': update.effective_user,
            'chat': update.effective_chat,
            'update': update
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
  #  LOGGER.info(
  #      f"IN: {update.effective_message.text} (user={user}, chat={chat})")


def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            bot.send_document(
                chat_id=update.effective_chat.id,
		document=out_file,
	        thumb=thumb
	    )
    else:
       # LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
	      f"*Output*:\n\n`{msg}`"
	    ),
            parse_mode=ParseMode.MARKDOWN,
	    reply_to_message_id=update.effective_message.message_id
	)


@dev_plus
def evaluate(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(eval, bot, update), bot, update)


@dev_plus
def execute(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(exec, bot, update), bot, update)


def cleanup_code(code):
    if code.startswith('```') and code.endswith('```'):
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')


def do(func, bot, update):
    log_input(update)
    content = "".join(update.message.text.split(maxsplit=1)[1:])
    #content = update.message.text.split(' ', 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    os.chdir(os.getcwd())
    with open(
            os.path.join(os.getcwd(),
                         'VegetaRobot/modules/helper_funcs/temp.txt'),
            'w') as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = f'def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return f'{e.__class__.__name__}: {e}'

    func = env['func']

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        value = stdout.getvalue()
        return f'{value}{traceback.format_exc()}'
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f'{value}'
            else:
                try:
                    result = f'{repr(eval(body, env))}'
                except:
                    pass
        else:
            result = f'{value}{func_return}'
        if result:
            return result


@dev_plus
def clear(update: Update, context: CallbackContext):
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)
    
# telethon eval

@client.on(events.NewMessage(from_users=DEV_USERS, pattern="^/teval ?(.*)"))
async def eval(event):
    if event.fwd_from:
        return
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return
    catevent = await client.send_message(event.chat.id, "`Running ...`", reply_to=event)
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**•  Eval : **\n`{cmd}` \n\n**•  Result : **\n`{evaluation}` \n"
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
            )
    else:
        await catevent.edit(final_output)


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, client, p)




EVAL_HANDLER = CommandHandler(('e', 'ev', 'eva', 'eval'), evaluate, run_async=True)
EXEC_HANDLER = CommandHandler(('x', 'ex', 'exe', 'exec', 'py'), execute, run_async=True)
CLEAR_HANDLER = CommandHandler('clearlocals', clear)

dispatcher.add_handler(EVAL_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)

__mod_name__ = "🔥 Eval"
