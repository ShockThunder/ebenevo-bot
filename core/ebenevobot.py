import telebot

from core import enviroment

bot = telebot.TeleBot(enviroment.token, threaded=False)
report_channel = enviroment.admin_channel_id
whitelist = enviroment.whitelist