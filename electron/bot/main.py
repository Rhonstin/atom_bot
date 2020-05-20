#from temp_to_svg import generate_day_png,generate_co2
import logging
from pymongo import MongoClient
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from time import localtime,strftime



def send(bot, update):
    flag = 0
    message = update.message.text
    if message == "📜":
        flag = 1
        get_keyboard(bot,update, flag)
    elif message == "📉":
        flag = 2
        get_keyboard(bot,update, flag)
    elif message == "🌡":
        button(bot, update, "temp")
    elif message == "⚗️":
        button(bot, update, 'humidity')






logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)









def get_keyboard(_bot, update, flag):
    if flag == 0:
        update.message.reply_text('Please choose another option')

    elif flag == 1:
        keyboard = [[KeyboardButton("🌡"),
                    KeyboardButton("⚗️")],
                    [KeyboardButton("🗜️", callback_data='preassure'),
                    KeyboardButton("🏭", callback_data='CO2')]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True)
        update.message.reply_text('Please choose option:', reply_markup=reply_markup)

    elif flag == 2:
        keyboard = [[KeyboardButton("5 minuts", callback_data=5),
                    KeyboardButton("15 minuts", callback_data=15),
                    KeyboardButton("30 hours", callback_data=30),
                    KeyboardButton("1 hours", callback_data=60)],
                    [KeyboardButton("3 hours", callback_data=180),
                    KeyboardButton("6 hours", callback_data=360),
                    KeyboardButton("9 hours", callback_data=540),
                    KeyboardButton("12 hours", callback_data=720),]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True)
        update.message.reply_text('Please choose option:', reply_markup=reply_markup)








def button(bot, update ,message):
    all_tables = get_last()
    param = ""
    if message == 'CO2':
        text = "home : {}{} ".format(all_tables[message],"ppm")
    else:
        if message == "temp":
            param = "°C"
        elif message == 'humidity':
            param = "%"
        elif message == "preassure":
            param ="mmHg"
        text = "street : home \n{:5.0f}{} : {:5.0f}{}".format( all_tables[message + "_i"], param, all_tables[message], param)
    update.message.reply_text(text=text)
    start(bot, update)

# Command /start & /help

def start(_bot, update):
    keyboard = [[KeyboardButton("📜")],[KeyboardButton("📉")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True)
    update.message.reply_text('Please choose option:', reply_markup=reply_markup)

def help(_bot, update):
    update.message.reply_text("Use /start to test this bot.")

def error(_bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Work with mongodb

client = MongoClient(host=['v140616.hosted-by-vdsina.ru:27017'])
db = client["bot_local"]    
posts = db.archive
def get_last():
    six_press = []    
    for post in posts.find():
        try:
            six_press.append(post)

        except KeyError:
            continue  
    return six_press[-1]

#main

def main():
    updater = Updater("558382857:AAHv4_JGvg71yiYyuBIA0aT0HwVTljI7ocU")
    dp = updater.dispatcher    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, send))
    dp.add_handler(CommandHandler('help', help))
    dp.add_error_handler(error)
    updater.start_polling()

if __name__ == '__main__':
    main()
