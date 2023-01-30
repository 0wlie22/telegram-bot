import telebot
import requests
import os
from datetime import date, timedelta

today = date.today()
end_date = today + timedelta(days=10)

URL = "https://www.akropoleriga.lv/api/v1/ice-sessions?city_id=7&language_id=70&locale=lv&withPrices=1&start=" + \
      str(today) + "T00:00:00&end=" + str(end_date) + "T00:00:00&end=2023-02-29T00:00:00&timeZone=Europe/Kiev"

r = requests.get(URL).json()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"), parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    session_count = 1
    message_list: str = ""
    for i in range(0, len(r)):
        if r[i]['title'] == "Publiskā slidotava":
            start: str = r[i]['starts_at']
            end: str = r[i]['ends_at']
            spots: str = r[i]['reservations']
            message_item: str = start[5:10] + "\t" + start[12:16] + "\t-\t" + end[12:16] + "\t|\t" + spots + "\n"
            message_list += message_item
            session_count += 1
    bot.reply_to(message, message_list)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
