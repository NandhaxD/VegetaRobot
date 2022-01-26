# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json #by ctzfamioy
import os


def get_user_list(config, key):
    with open('{}/VegetaRobot/{}'.format(os.getcwd(), config),
              'r') as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    #Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 7126006  # integer value, dont use ""
    API_HASH = "f92b05be529835381859ead64a195fa2"
    TOKEN = "2128359921:AAFo-u0Y0e3ZNh2JScMGYoe9oy2UBQuur_4"  #This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1491497760  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "ctzfamily"
    SUPPORT_CHAT = 'vegetasupport'  #Your own group for support, do not add the @
    UPDATES_CHANNEL = 'vegetaUpdates' #Your own channel for Updates of bot, Do not add @
    JOIN_LOGGER = -1001543354286  #Prints any new group the bot is added to, prints just the name and ID.
    REM_BG_API_KEY = "dxsh728mZMDmj4ijSZCNPZig"
    STRING_SESSION = "1BVtsOIgBu2dMF7FyBJZOig7ITZDtkaJQ-9y2i_kNIP_zTcUQ5-QG-yl04x5jbZgsnIF1n8mVg8WVQbMZB8Hi5edGcQUy8NM9QXj5IILEeIHtEBs_dFMcZ0z-wKEZ4iL2tvbNyQOIqWAYGjnsR3c_-qmZCn3gnEjOWWN9HxLe3_6C7JVw2rhuVQVAR4dWWtVEjxWmnvUL32Dlp45STq92rBbzHyHhEUOMb6CJUKh7-b-1yS8vi7Yc_7KkL2ls8QFGg1s7i-paDZqZFnJrN0IyLj5WK01ZirX62Mqw7z9Ii58CETCQutPBU29Kwyp28vtvNjegZcANwgqZZN38vJ0G9TzwJTSX920="
    TEMP_DOWNLOAD_DIRECTORY = ""
    EVENT_LOGS = -1001543354286  #Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    SQLALCHEMY_DATABASE_URI = ''
    LOAD = []
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    WEBHOOK = None
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key -
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    BOT_ID = "2128359921"
    
    DRAGONS = get_user_list('elevated_users.json', 'sudos')

    DEV_USERS = get_user_list('elevated_users.json', 'devs')
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list('elevated_users.json', 'supports')
    #List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list('elevated_users.json', 'tigers')
    WOLVES = get_user_list('elevated_users.json', 'whitelists')
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  #Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    STRICT_GMUTE = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = ''  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    ARQ_API_URL = "https://thearq.tech"
    ARQ_API_KEY = "FEUAAQ-IYDNKK-VTYUKD-LMMXLA-ARQ"
    CASH_API_KEY = 'awoo'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'awoo'  # Get your API key from https://timezonedb.com/api
    OPENWEATHERMAP_ID = 'awoo'
    WALL_API = 'awoo'  #For wallpapers, get one from https://wall.alphacoders.com/api.php
    AI_API_KEY = 'awoo'  #For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
