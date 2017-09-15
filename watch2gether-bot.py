#test
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from telegram.ext import Updater
from telegram.ext import CommandHandler, InlineQueryHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import time
import string
import logging

def create_room():
    chrome_options = Options() 
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path=r"C:\Users\Chris\Desktop\teleBot\teleBot\teleBot\chromedriver.exe", chrome_options = chrome_options)
    driver.wait = WebDriverWait(driver, 5)

    driver.get('https://www.watch2gether.com') #going to site
    driver.find_element_by_css_selector('.ui.primary.button').click()
    room_url = driver.current_url
    driver.quit()
    
    keyboard = [[InlineKeyboardButton("Room Url", room_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def initial_keyboard():
    keyboard = [[InlineKeyboardButton("Create Room", callback_data='Create')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def button(bot, update):
    query = update.callback_query

    if query.data == 'Create':
        #query.message.reply_text('Your room is ready', reply_markup = create_room())
        bot.send_message(chat_id = query.message.chat_id, text = "I'm opening room for you, please hang on.")
        bot.send_message(chat_id = query.message.chat_id, text = 'Your room is ready', reply_markup = create_room())

def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = 'watch2gether-bot is ready for serve you.', reply_markup= initial_keyboard())

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token = '444813380:AAGY4Fnq6M-8hrZjX2ze_UWCdX3WAWxeuK4')
dispatcher = updater.dispatcher

button_handler = CallbackQueryHandler(button)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
print('start')
