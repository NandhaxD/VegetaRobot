import html
import sys
import json
from datetime import datetime
from platform import python_version
from typing import List
from uuid import uuid4
from pyrogram import __version__ as pyrover

import requests
from telegram import InlineQueryResultPhoto, InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram import __version__
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

import VegetaRobot.modules.sql.users_sql as sql
from VegetaRobot import (
    OWNER_ID,
    DRAGONS,
    DEMONS,
    DEV_USERS,
    TIGERS,
    WOLVES,
    sw, LOGGER
)
from VegetaRobot.modules.helper_funcs.misc import article
from VegetaRobot.modules.helper_funcs.decorators import vegetainline as kiginline


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        text = text.replace(prefix, "", 1)
    return text

@kiginline()
def inlinequery(update: Update, _) -> None:
    """
    Main InlineQueryHandler callback.
    """
    query = update.inline_query.query
    user = update.effective_user

    results: List = []
    inline_help_dicts = [
        {
            "title": "SpamProtection INFO",
            "description": "Look up a person/bot/channel/chat on @Intellivoid SpamProtection API",
            "message_text": "Click the button below to look up a person/bot/channel/chat on @Intellivoid SpamProtection API using "
                            "username or telegram id",
            "thumb_urL": "https://telegra.ph/file/3ce9045b1c7faf7123c67.jpg",
            "keyboard": ".spb",
        },
        {
            "title": "About & info",
            "description": "About And informations",
            "message_text": "Click the below button for about and commads",
            "thumb_urL": "http://telegra.ph/file/6e8a69b73969cc433d2cf.jpg",
            "keyboard": "about",
        },
    ]
        
          
       

    inline_funcs = {
        "disaster": disaster,
        "health": health,
        "spb": spb,
        "info": inlineinfo,
        "about": about,
        "anilist": media_query,
    }

    if (f := query.split(" ", 1)[0]) in inline_funcs:
        inline_funcs[f](remove_prefix(query, f).strip(), update, user)
    else:
        for ihelp in inline_help_dicts:
            results.append(
                article(
                    title=ihelp["title"],
                    description=ihelp["description"],
                    message_text=ihelp["message_text"],
                    thumb_url=ihelp["thumb_urL"],
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Click Here",
                                    switch_inline_query_current_chat=ihelp[
                                        "keyboard"
                                    ],
                                )
                            ]
                        ]
                    ),
                )
            )

        update.inline_query.answer(results, cache_time=5)

        
        
        
def disaster(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    disaster_text = """
    VegetaRobot has access Ranks we call as "Disaster Levels"
• A-Rank - can access the bots server
• God - Only one exists, bot owner.
• S-Rank - can gban, manage Disasters lower than them.
• B-Rank - Have access to globally ban users.
• TIGERS - they can unban themselves if banned.
• WOLVES - Cannot be banned, muted, flood kicked.
"""
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"disaster",
            input_message_content=InputTextMessageContent(test_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True),
        ),
    ]


def health(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    health_text = """
        📈 What is that health bar that VegetaRobot displays on /info❔
That is a new weeb tech called "HP system", aka Health points system.
Explaining what the panel is
Health: avail_hp/max_hp
[health bar] percentage

What does this even do ❔
It's an interactive way of showing how complete your profile is.
Users with no PFP, no username, no bio on Saitama or no what others say will have less health as their profile is considered as "incomplete".

How we determine Max HP
((Number of chats seen in +10 )*10)
Basically the more groups Miku sees you in, the higher your max hp is.
You don't need to stay in the group, you can just join, send a message and leave and max hp will slightly increase.

Penalties from available HP:
-25% if no username
-25% if no profile pic
-20% if no setme exists
-10% if no what others say exists
 -7% if user is AFK
 -5% if the user is AFK with reason

Bad status effects:
Gbanned users will always have 5% HP from max HP
Example: If HP is 100 but gbanned
Available HP is 5% of 100 = 5HP

Why was this added❔
To make the info panel more fun but mainly to urge our users to have a properly written profile, good profiles help you connect to users around you (plus looking like some spammer ID isnt a good experience, is it?)
    """
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"health",
            input_message_content=InputTextMessageContent(health_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True),
        ),
    ]

    update.inline_query.answer(results, cache_time=5)
    
def inlineinfo(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    bot = context.bot
    query = update.inline_query.query
    LOGGER.info(query)
    user_id = update.effective_user.id

    try:
        search = query.split(" ", 1)[1]
    except IndexError:
        search = user_id

    try:
        user = bot.get_chat(int(search))
    except (BadRequest, ValueError):
        user = bot.get_chat(user_id)

    chat = update.effective_chat
    sql.update_user(user.id, user.username)

    text = (
        f"<b>Information:</b>\n"
        f"✪ ID: <code>{user.id}</code>\n"
        f"✪ First Name: {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n✪ Last Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n✪ Username: @{html.escape(user.username)}"

    text += f"\n✪ Permanent user link: {mention_html(user.id, 'link')}"

    nation_level_present = False

    if user.id == OWNER_ID:
        text += f"\n\nThis person is 'MASTER'"
        nation_level_present = True
    elif user.id in DEV_USERS:
        text += f"\n\nThis Person is Developer of Vegeta"
        nation_level_present = True
    elif user.id in DRAGONS:
        text += f"\n\nThis person is 'A-Rank'"
        nation_level_present = True
    elif user.id in DEMONS:
        text += f"\n\nThis person is 'B-Rank'"
        nation_level_present = True
    elif user.id in TIGERS:
        text += f"\n\nThis person is Tiger Level Disaster"
        nation_level_present = True
    elif user.id in WOLVES:
        text += f"\n\nThe Nation level of this person is Wolf Level Disaster"
        nation_level_present = True

    if nation_level_present:
        text += ' [<a href="https://t.me/vegetaUpdates/167">[ RANKS ]</a>]'.format(bot.username)

    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += "<b>\n\n✪ SpamWatched:\n</b> Yes"
            text += f"\n✪ Reason: <pre>{spamwtc.reason}</pre>"
            text += "\n✪ Appeal at @SpamWatchSupport"
        else:
            text += "<b>\n\n✪ SpamWatched:</b> No"
    except:
        pass  # don't crash if api is down somehow...

    num_chats = sql.get_user_num_chats(user.id)
    text += f"\n✪ <b>Chat count</b>: <code>{num_chats}</code>"




    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʀᴇᴘᴏʀᴛ ᴇʀʀᴏʀ",
                    url=f"https://t.me/vegetasupport",
                ),
                InlineKeyboardButton(
                    text="sᴇᴀʀxʜ ᴀɢᴀɪɴ",
                    switch_inline_query_current_chat=".info ",
                ),

            ],
        ]
        )

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"User info of {html.escape(user.first_name)}",
            input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.HTML,
                                                          disable_web_page_preview=True),
            reply_markup=kb
        ),
    ]

    update.inline_query.answer(results, cache_time=5)


def about(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    about_text = f"""

        *Bot State:* `Alive`
    *Python:* `{python_version()}`
    *Pyrogram:* `{pyrover}`
    *Platform:* `{sys.platform}`
    *python-telegram-bot:* `v{str(__version__)}`
    """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ɪɴғᴏ",
                    switch_inline_query_current_chat=".info ",
                ),
                
                InlineKeyboardButton(
                    text="ᴀɴɪʟɪsᴛ",
                    switch_inline_query_current_chat=".anilist ",
                ),
                
                ],
                 [
                     
                InlineKeyboardButton(
                    text="sᴜᴘᴘᴏʀᴛ",
                    url="t.me/VegetaSupport",
                ),
                InlineKeyboardButton(
                    text="ᴜᴘᴅᴀᴛᴇs",
                    url="t.me/VegetaUpdates",
                ),
                     
                ],
                 [
                InlineKeyboardButton(
                    text='ɪɴʟɪɴᴇ ɢᴏ',
                    switch_inline_query_current_chat=""
                ),

            ],
        ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            thumb_url="http://telegra.ph/file/6e8a69b73969cc433d2cf.jpg",
            photo_url="http://telegra.ph/file/6e8a69b73969cc433d2cf.jpg",
            caption=about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb
        )
    )
    update.inline_query.answer(results)


def spb(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    srdata = None
    apst = requests.get(f'https://api.intellivoid.net/spamprotection/v1/lookup?query={context.bot.username}')
    api_status = apst.status_code
    if (api_status != 200):
        stats = f"API RETURNED {api_status}"
    else:
        try:
            search = query.split(" ", 1)[1]
        except IndexError:
            search = user_id

        srdata = search or user_id
        url = f"https://api.intellivoid.net/spamprotection/v1/lookup?query={srdata}"
        r = requests.get(url)
        a = r.json()
        response = a["success"]
        if response is True:
            date = a["results"]["last_updated"]
            stats = f"*✪ Intellivoidâ€¢ SpamProtection Info*:\n"
            stats += f'✪ *Updated on*: `{datetime.fromtimestamp(date).strftime("%Y-%m-%d %I:%M:%S %p")}`\n'

            if a["results"]["attributes"]["is_potential_spammer"] is True:
                stats += f" ✪ *User*: `USERxSPAM`\n"
            elif a["results"]["attributes"]["is_operator"] is True:
                stats += f" ✪ *User*: `USERxOPERATOR`\n"
            elif a["results"]["attributes"]["is_agent"] is True:
                stats += f" ✪ *User*: `USERxAGENT`\n"
            elif a["results"]["attributes"]["is_whitelisted"] is True:
                stats += f" ✪ *User*: `USERxWHITELISTED`\n"

            stats += f' ✪ *Type*: `{a["results"]["entity_type"]}`\n'
            stats += (
                f' ✪ *Language*: `{a["results"]["language_prediction"]["language"]}`\n'
            )
            stats += f' ✪ *Language Probability*: `{a["results"]["language_prediction"]["probability"]}`\n'
            stats += f"*Spam Prediction*:\n"
            stats += f' ✪ *Ham Prediction*: `{a["results"]["spam_prediction"]["ham_prediction"]}`\n'
            stats += f' ✪ *Spam Prediction*: `{a["results"]["spam_prediction"]["spam_prediction"]}`\n'
            stats += f'*Blacklisted*: `{a["results"]["attributes"]["is_blacklisted"]}`\n'
            if a["results"]["attributes"]["is_blacklisted"] is True:
                stats += (
                    f' ✪ *Reason*: `{a["results"]["attributes"]["blacklist_reason"]}`\n'
                )
                stats += f' ✪ *Flag*: `{a["results"]["attributes"]["blacklist_flag"]}`\n'
            stats += f'*PTID*:\n`{a["results"]["private_telegram_id"]}`\n'

        else:
            stats = "`cannot reach SpamProtection API`"

    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʀᴇᴘᴏʀᴛ ᴇʀʀᴏʀ",
                    url=f"https://t.me/vegetasupport",
                ),
                InlineKeyboardButton(
                    text="Sᴇᴀʀᴄʜ ᴀɢᴀɪɴ",
                    switch_inline_query_current_chat=".spb ",
                ),

            ],
        ])

    a = "the entity was not found"
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"SpamProtection API info of {srdata or a}",
            input_message_content=InputTextMessageContent(stats, parse_mode=ParseMode.MARKDOWN,
                                                          disable_web_page_preview=True),
            reply_markup=kb
        ),
    ]

    update.inline_query.answer(results, cache_time=5)



MEDIA_QUERY = '''query ($search: String) {
  Page (perPage: 10) {
    media (search: $search) {
      id
      title {
        romaji
        english
        native
      }
      type
      format
      status
      description
      episodes
      bannerImage
      duration
      chapters
      volumes
      genres
      synonyms
      averageScore
      airingSchedule(notYetAired: true) {
        nodes {
          airingAt
          timeUntilAiring
          episode
        }
      }
      siteUrl
    }
  }
}'''


def media_query(query: str, update: Update, context: CallbackContext) -> None:
    """
    Handle anime inline query.
    """
    results: List = []

    try:
        results: List = []
        r = requests.post('https://graphql.anilist.co',
                          data=json.dumps({'query': MEDIA_QUERY, 'variables': {'search': query}}),
                          headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        res = r.json()
        data = res['data']['Page']['media']
        res = data
        for data in res:
            title_en = data["title"].get("english") or "N/A"
            title_ja = data["title"].get("romaji") or "N/A"
            format = data.get("format") or "N/A"
            type = data.get("type") or "N/A"
            bannerimg = data.get("bannerImage") or "https://telegra.ph/file/cc83a0b7102ad1d7b1cb3.jpg"
            try:
                des = data.get("description").replace("<br>", "").replace("</br>", "")
                description = des.replace("<i>", "").replace("</i>", "") or "N/A"
            except AttributeError:
                description = data.get("description")

            try:
                description = html.escape(description)
            except AttributeError:
                description = description or "N/A"

            if len((str(description))) > 700:
                description = description [0:700] + "....."

            avgsc = data.get("averageScore") or "N/A"
            status = data.get("status") or "N/A"
            genres = data.get("genres") or "N/A"
            genres = ", ".join(genres)
            img = f"https://img.anili.st/media/{data['id']}" or "https://telegra.ph/file/cc83a0b7102ad1d7b1cb3.jpg"
            aurl = data.get("siteUrl")


            kb = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ʀᴇᴀᴅ ᴍᴏʀᴇ",
                            url=aurl,
                        ),
                        InlineKeyboardButton(
                            text="Sᴇᴀʀᴄʜ ᴀɢᴀɪɴ",
                            switch_inline_query_current_chat=".anilist",
                        ),

                    ],
                ])

            txt = f"<b>{title_en} | {title_ja}</b>\n"
            txt += f"<b>Format</b>: <code>{format}</code>\n"
            txt += f"<b>Type</b>: <code>{type}</code>\n"
            txt += f"<b>Average Score</b>: <code>{avgsc}</code>\n"
            txt += f"<b>Status</b>: <code>{status}</code>\n"
            txt += f"<b>Genres</b>: <code>{genres}</code>\n"
            txt += f"<b>Description</b>: <code>{description}</code>\n"
            txt += f"<a href='{img}'>&#xad</a>"

            results.append(
                InlineQueryResultArticle
                    (
                    id=str(uuid4()),
                    title=f"{title_en} | {title_ja} | {format}",
                    thumb_url=img,
                    description=f"{description}",
                    input_message_content=InputTextMessageContent(txt, parse_mode=ParseMode.HTML,
                                                                  disable_web_page_preview=False),
                    reply_markup=kb
                )
            )
    except Exception as e:

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ʀᴇᴘᴏʀᴛ ᴇʀʀᴏʀ",
                        url="https://t.me/vegetasupport",
                    ),
                    InlineKeyboardButton(
                        text="Sᴇᴀʀᴄʜ ᴀɢᴀɪɴ",
                        switch_inline_query_current_chat=".anilist ",
                    ),

                ],
            ])

        results.append(

            InlineQueryResultArticle
                (
                id=str(uuid4()),
                title=f"Media {query} not found",
                input_message_content=InputTextMessageContent(f"Media {query} not found due to {e}", parse_mode=ParseMode.MARKDOWN,
                                                              disable_web_page_preview=True),
                reply_markup=kb
            )

        )

    update.inline_query.answer(results, cache_time=5)

