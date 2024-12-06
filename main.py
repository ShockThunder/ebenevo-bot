from core import ebenevobot
from modules import anekdots
from modules import adm_commands
from modules import members
from modules import party
import telebot

ebenevobot.bot.infinity_polling(none_stop=True, allowed_updates=telebot.util.update_types)