#import time
#import datetime
import logging
import sqlite3
import datetime
import time
import threading
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, RegexHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

def create_room(bot, update):
    try:
        bot.send_message(chat_id = update.message.chat_id, 
                            text = "I'm opening room for you, please hang on.")
        chrome_options = Options() 
        chrome_options.add_argument("--headless")
        if os.name == "nt":
                driver = webdriver.Chrome(executable_path=r"C:\Users\Chris\Desktop\teleBot\teleBot\teleBot\chromedriver.exe", chrome_options = chrome_options)
        elif os.name == "posix":
                driver = webdriver.Chrome("./chromedriver" , chrome_options = chrome_options)
        driver.wait = WebDriverWait(driver, 5)

        driver.get('https://www.watch2gether.com') #going to site
        driver.find_element_by_css_selector('.ui.primary.button').click()
        room_url = driver.current_url
        driver.quit()

        keyboard = [[InlineKeyboardButton("Room Url", room_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id = update.message.chat_id, text = 'Your room is ready', reply_markup = reply_markup)

        create_time = update.message.date
        creater = update.message.chat['first_name'] + update.message.chat['last_name']

        data_store(create_time, room_url, creater)
    except Exception as e:
        print(e)

def data_store(create_time, url, creater):
    try:
        conn = sqlite3.connect("watch2gether.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS TB_ROOM
                (PK_ROOMID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                DATE_CREATED DATETIME NOT NULL,
                URL TEXT NOT NULL,
                CREATER TEXT NOT NULL);''')
        cursor.execute("INSERT INTO TB_ROOM(DATE_CREATED,URL,CREATER) VALUES (?,?,?);",(create_time, url, creater))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def view_data():
    try:
        sql_data = []
        conn = sqlite3.connect("watch2gether.db")
        cursor = conn.cursor()
        for row in cursor.execute("SELECT DATE_CREATED,URL,CREATER FROM TB_ROOM;"):
            sql_data.append(row)
        return sql_data
    except Exception as e:
        print(e)

def delete_data():
    while True:
        #try:
        #    conn = sqlite3.connect("watch2gether.db")
        #    cursor = conn.cursor()
        #    time_now = datetime.datetime.now()
        #    for row in cursor.execute("SELECT DATE_CREATED FROM TB_ROOM;"):
        #        create_time, = row
        #        if (time_now - datetime.datetime.strptime(create_time,'%Y-%m-%d %H:%M:%S')) > datetime.timedelta(days = 1): cursor.execute("DELETE FROM TB_ROOM WHERE DATE_CREATED = ?",(create_time))
        #    cursor.commit()
        #    time.sleep(5)
        #except Exception as e:
        #    print(e)
        #    time.sleep(5)
        #    continue
        conn = sqlite3.connect("watch2gether.db")
        cursor = conn.cursor()
        time_now = datetime.datetime.now()
        for row in cursor.execute("SELECT DATE_CREATED FROM TB_ROOM;"):
            create_time, = row
            if (time_now - datetime.datetime.strptime(create_time,'%Y-%m-%d %H:%M:%S')) > datetime.timedelta(days = 1): cursor.execute("DELETE FROM TB_ROOM WHERE DATE_CREATED = '%s'"%create_time)
        conn.commit()
        time.sleep(5)

def view(bot, update):
    message = ""
    for row in view_data():
        date, url, creater = row
        message += "Date: %s Created by: %s  url: %s \r\n\r\n"%(date, creater, url)
    bot.send_message(chat_id = update.message.chat_id, text = message)

def start(bot, update):
    keyboard = [['Create', 'View']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    start_msg = r'watch2gether-bot is at your service.\
     Click Create button to create a room.\
     Click View button to view aviliable rooms'
    bot.send_message(chat_id = update.message.chat_id, text = start_msg, reply_markup = markup)

def main():
    updater = Updater(token = '441243370:AAFADtpDKCcfVxdlmvnuY36fVhDQPeU3cJM')
    dispatcher = updater.dispatcher

    sql_deletion = threading.Thread(target = delete_data)
    sql_deletion.daemon = True

    start_handler = CommandHandler('start', start)
    create_handler = RegexHandler('^Create$', create_room)
    view_handler = RegexHandler('^View$', view)
    dispatcher.add_handler(create_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(view_handler)

    sql_deletion.start()
    updater.start_polling()
    print('start')

if __name__ == '__main__':
    main()
