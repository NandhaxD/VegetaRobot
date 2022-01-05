from geopy.geocoders import Nominatim #boom
from telegram import ( 
    ParseMode,
    Location,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CommandHandler, run_async

from VegetaRobot import dispatcher
from VegetaRobot.modules.helper_funcs.chat_status import user_admin

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"


@run_async
@user_admin
def gps(update, context, *args, **kwargs):

    args = context.args
    update.effective_message
    if len(args) == 0:
        update.effective_message.reply_text(
            "That was a funny joke, but no really, put in a location"
        )
    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = " ".join(args)
        geoloc = geolocator.geocode(location)
        chat_id = update.effective_chat.id
        lon = geoloc.longitude
        lat = geoloc.latitude
        the_loc = Location(lon, lat)
        gm = "https://www.google.com/maps/search/{},{}".format(lat, lon)
        dispatcher.bot.send_location(chat_id, location=the_loc,
                                 disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(
              text="Location",url=f"{gm}")]]
     

    
GPS_HANDLER = CommandHandler("gps", gps)

dispatcher.add_handler(GPS_HANDLER)




__mod_name__ = "GPS"

