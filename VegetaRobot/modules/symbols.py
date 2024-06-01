import json
from pyrogram import types, filters
from VegetaRobot import pgram as bot

# Load the data from the JSON file

with open("./VegetaRobot/utils/symbols_data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

num_columns = 8
page_size = 5

@bot.on_callback_query(filters.regex(r'^syback:\d+:\d+') | filters.regex(r'^synext:\d+:\d+'))
async def sym_next_back(_, query):
    user_id = int(query.data.split(':')[1])
    target_index = int(query.data.split(':')[2])

    if query.from_user.id != user_id:
        return await query.answer('Sorry this is not your Query.')

    # Calculate the start index of the current page
    if query.data.startswith('syback'):
        target_index = max(0, target_index - page_size)
    else:
        target_index = min(len(data) - page_size, target_index + page_size)

    buttons = []
    for index, (title, content) in enumerate(data.items()):
        if index < target_index:
            continue
        if index >= target_index + page_size:
            break
        buttons.append(
            types.InlineKeyboardButton(
                title, callback_data=f'symbol:{user_id}:{index}'
            )
        )

    columns_btn = [[button] for button in buttons]
    
    # Add navigation buttons
    navigation_buttons = []
    if target_index > 0:
        navigation_buttons.append(
            types.InlineKeyboardButton(
                "⬅️ Back", callback_data=f'syback:{user_id}:{target_index}'
            )
        )
    if target_index + page_size < len(data):
        navigation_buttons.append(
            types.InlineKeyboardButton(
                "Next ➡️", callback_data=f'synext:{user_id}:{target_index}'
            )
        )

    if navigation_buttons:
        columns_btn.append(navigation_buttons)

    reply_markup = types.InlineKeyboardMarkup(columns_btn)

    await query.message.edit_text(
        "**Here are some symbols for you to explore. I hope you find something special today!**",
        reply_markup=reply_markup
    )

@bot.on_message(filters.command("symbols"))
async def symbols(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    buttons = []
    for index, (title, content) in enumerate(data.items()):
        if index >= page_size:
            break
        buttons.append(
            types.InlineKeyboardButton(
                title, callback_data=f'symbol:{user_id}:{index}'
            )
        )

    columns_btn = [[button] for button in buttons]
    
    # Add navigation buttons if there are more pages
    navigation_buttons = []
    if page_size < len(data):
        navigation_buttons.append(
            types.InlineKeyboardButton(
                "Next ➡️", callback_data=f'synext:{user_id}:{0}'
            )
        )
    if navigation_buttons:
        columns_btn.append(navigation_buttons)

    reply_markup = types.InlineKeyboardMarkup(columns_btn)

    await bot.send_message(
        chat_id=chat_id,
        text="**Here are some symbols for you to explore. I hope you find something special today!**",
        reply_markup=reply_markup
    )
    

@bot.on_callback_query(filters.regex('^symbol'))
async def cb_symbols(_, query):
    user_id = int(query.data.split(':')[1])
    target_index = int(query.data.split(':')[2])
    if query.from_user.id != user_id:
        return await query.answer(
            'Sorry, this is not your Query.', show_alert=True)

    text = ''

    for index, (title, content) in enumerate(data.items()):
        if index == target_index:
            text += f'**{title}**:\n\n'
            symbols = content.split()
            for i in range(0, len(symbols), num_columns):
                row = symbols[i:i + num_columns]
                formatted_row = '  '.join(f'`{symbol}`' for symbol in row)
                text += f'{formatted_row}\n'
            break

    return await query.message.edit_text(
         text=text,
    reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton(
        text='Back ⬅️', callback_data=f'syback:{user_id}:{target_index}'
    )]])
    )
