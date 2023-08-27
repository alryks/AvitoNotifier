import threading
import schedule

from notify import notify

import telebot
from telebot.types import Message

from settings import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def start(message: Message):
    bot.send_message(message.chat.id, "I'm Avito Notifier Bot")


schedule.every(10).minutes.do(notify, bot)


def run_scheduler():
    while True:
        schedule.run_pending()


scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()


bot.infinity_polling()
