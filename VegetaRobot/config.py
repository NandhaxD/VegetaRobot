# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
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
    TOKEN = "2128359921:AAERyRO1dEAxOouaUOE4B8dxocXazE72Gro"  #This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1491497760  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "ctzfamily"
    SUPPORT_CHAT = 'vegetasupport'  #Your own group for support, do not add the @
    UPDATES_CHANNEL = 'vegetaUpdates' #Your own channel for Updates of bot, Do not add @
    JOIN_LOGGER = -1001739802989  #Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = -1001739802989  #Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    SQLALCHEMY_DATABASE_URI = 'postgres://yjbklqzqytefhl:4a729e337257be81fdc359cd856e34a0b5a261419d5138f25b81193bb27774e8@ec2-52-54-38-229.compute-1.amazonaws.com:5432/d8pnbft2italbv'#'postgres://vagszglpwcqjuv:7ac64f23996ef264ec3b67c65f3a6eaa1ac41a77588553e09623558127ff6d1f@ec2-52-202-198-60.compute-1.amazonaws.com:5432/d7pmn914up6sq4'
    LOAD = []
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    WEBHOOK = None
    INFOPIC = True
    TEMP_DOWNLOAD_DIRECTORY = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
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
