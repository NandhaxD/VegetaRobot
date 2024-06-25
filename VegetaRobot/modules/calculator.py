


from VegetaRobot import pgram as app
from pyrogram import filters, types, enums, errors
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


import logging
import re


LOGGER = logging.getLogger("NandhaXBOT")

def calcExpression(text):
    try:
        return float(eval(text))
    except (SyntaxError, ZeroDivisionError):
        return ""
    except TypeError:
        return float(eval(text.replace('(', '*(')))
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        return ""

def calc_btn(uid):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("DEL", callback_data=f"calc|{uid}|DEL"),
                InlineKeyboardButton("AC", callback_data=f"calc|{uid}|AC"),
                InlineKeyboardButton("(", callback_data=f"calc|{uid}|("),
                InlineKeyboardButton(")", callback_data=f"calc|{uid}|)"),
            ],
            [
                InlineKeyboardButton("7", callback_data=f"calc|{uid}|7"),
                InlineKeyboardButton("8", callback_data=f"calc|{uid}|8"),
                InlineKeyboardButton("9", callback_data=f"calc|{uid}|9"),
                InlineKeyboardButton("÷", callback_data=f"calc|{uid}|/"),
            ],
            [
                InlineKeyboardButton("4", callback_data=f"calc|{uid}|4"),
                InlineKeyboardButton("5", callback_data=f"calc|{uid}|5"),
                InlineKeyboardButton("6", callback_data=f"calc|{uid}|6"),
                InlineKeyboardButton("×", callback_data=f"calc|{uid}|*"),
            ],
            [
                InlineKeyboardButton("1", callback_data=f"calc|{uid}|1"),
                InlineKeyboardButton("2", callback_data=f"calc|{uid}|2"),
                InlineKeyboardButton("3", callback_data=f"calc|{uid}|3"),
                InlineKeyboardButton("-", callback_data=f"calc|{uid}|-"),
            ],
            [
                InlineKeyboardButton(".", callback_data=f"calc|{uid}|."),
                InlineKeyboardButton("0", callback_data=f"calc|{uid}|0"),
                InlineKeyboardButton("=", callback_data=f"calc|{uid}|="),
                InlineKeyboardButton("+", callback_data=f"calc|{uid}|+"),
            ],
        ]
    )


@app.on_message(filters.command(["calc", "calculate", "calculator"]))
async def calculate_handler(self, ctx):
    if not ctx.from_user:
        return
    await ctx.reply_text(
        text=f"Made by @{self.me.username}",
        reply_markup=calc_btn(ctx.from_user.id),
        disable_web_page_preview=True,
        quote=True
    )

@app.on_callback_query(filters.regex("^calc"))
async def calc_cb(self, query):
    _, uid, data = query.data.split("|")
    if query.from_user.id != int(uid):
        return await query.answer("Who are you??", show_alert=True, cache_time=5)
    try:
        text = query.message.text.split("\n")[0].strip().split("=")[0].strip()
        text = '' if f"Made by @{self.me.username}" in text else text
        inpt = text + query.data
        result = ""
        if data == "=":
            result = calcExpression(text)
            text = ""
        elif data == "DEL":
            text = text[:-1]
        elif data == "AC":
            text = ""
        else:
            dot_dot_check = re.findall(r"(\d*\.\.|\d*\.\d+\.)", inpt)
            opcheck = re.findall(r"([*/\+-]{2,})", inpt)
            if not dot_dot_check and not opcheck:
                if strOperands := re.findall(r"(\.\d+|\d+\.\d+|\d+)", inpt):
                    text += data
                    result = calcExpression(text)

        text = f"{text:<50}"
        if result:
            if text:
                text += f"\n{result:>50}"
            else:
                text = result
        text += f"\n\nMade by @{self.me.username}"
        await query.message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=calc_btn(query.from_user.id)
        )
    except Exception as error:
        LOGGER.error(error)


__help__ = """
➩ `/calc`:
 To calculate any expression ( math question )
"""

__mod_name__ = "Calc"
    
