#from temp_to_svg import generate_day_png,generate_co2
import logging
from pymongo import MongoClient
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , CallbackQueryHandler
from telegram.error import NetworkError, Unauthorized
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from time import localtime,strftime



def send(bot, update):
    flag = 0
    if update.message.text == "📜":
        flag = 1
        get_keyboard(bot,update, flag)
    elif update.message.text == "📉":
        flag = 2
        get_keyboard(bot,update, flag)        





logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)









def get_keyboard(bot, update, flag):
    if flag == 0:
        update.message.reply_text('Please choose another option')

    elif flag == 1:
        keyboard = [[InlineKeyboardButton("🌡", callback_data='temp'),
                    InlineKeyboardButton("⚗️", callback_data='humidity')],
                    [InlineKeyboardButton("🗜️", callback_data='preassure'),
                    InlineKeyboardButton("🏭", callback_data='CO2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose option:', reply_markup=reply_markup)

    elif flag == 2:
        keyboard = [[InlineKeyboardButton("5 minuts", callback_data=5),
                    InlineKeyboardButton("15 minuts", callback_data=15),
                    InlineKeyboardButton("30 hours", callback_data=30)
                    InlineKeyboardButton("1 hours", callback_data=60)],
                    [InlineKeyboardButton("3 hours", callback_data=180),
                    InlineKeyboardButton("6 hours", callback_data=360),
                    InlineKeyboardButton("9 hours", callback_data=540),
                    InlineKeyboardButton("12 hours", callback_data=720),]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose option:', reply_markup=reply_markup)








def button(bot, update):
    query = update.callback_query
    all_tables = get_last()
    param = ""
    if query.data == 'CO2':
        text = "home : {}{} ".format(all_tables[query.data],"ppm")
    else:
        if query.data == "temp":
            param = "°C"
        elif query.data == 'humidity':
            param = "%"
        elif query.data == "preassure":
            param ="mmHg"
        text = "street : home \n{:5.0f}{} : {:5.0f}{}".format( all_tables[query.data + "_i"], param, all_tables[query.data], param)
    query.edit_message_text(text=text)

# Command /start & /help

def start(bot, update):
    keyboard = [[KeyboardButton("📜")],[KeyboardButton("📉")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard = True)
    update.message.reply_text('Please choose option:', reply_markup=reply_markup)

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Work with mongodb

client = MongoClient(host=['mondog:27017'])
db = client["bot_local"]    
posts = db.archive
def get_last():
    six_press = []    
    for post in posts.find():
        try:
            six_press.append(post)
            print(six_press)
        except KeyError:
            continue  
    return six_press[-1]

#main

def main():
    updater = Updater("558382857:AAHv4_JGvg71yiYyuBIA0aT0HwVTljI7ocU")
    dp = updater.dispatcher    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, send))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('help', help))
    dp.add_error_handler(error)
    updater.start_polling()

if __name__ == '__main__':
    main()
