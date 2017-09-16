from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, InlineQueryHandler, CallbackQueryHandler, RegexHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)  

def create_room(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "I'm opening room for you, please hang on.")
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
    bot.send_message(chat_id = update.message.chat_id, text = 'Your room is ready', reply_markup = reply_markup)

def start(bot, update):
    keyboard = [['Create', 'View']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    start_msg = r'watch2gether-bot is at your service. Click Create button to create a room. Click View button to view aviliable rooms'
    bot.send_message(chat_id = update.message.chat_id, text = start_msg, reply_markup = markup)

def main():
    updater = Updater(token = '444813380:AAGY4Fnq6M-8hrZjX2ze_UWCdX3WAWxeuK4')
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    create_handler = RegexHandler('^Create$', create_room)
    dispatcher.add_handler(create_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    print('start')

if __name__ == '__main__':
    main()
