import telebot

from core import enviroment

bot = telebot.TeleBot(enviroment.token)
report_channel = enviroment.admin_channel_id
whitelist = enviroment.whitelist