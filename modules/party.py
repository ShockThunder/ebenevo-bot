import string
import random

from core import ebenevobot
from data import db_handler

bot = ebenevobot.bot
game_db = db_handler.game_db
User = db_handler.User

party_mode = True

def clean_message(message):
    # Убираем знаки препинания
    message = message.translate(str.maketrans('', '', string.punctuation))
    # Убираем лишние слова
    words_to_remove = ["чат", "я", "и"]
    for word in words_to_remove:
        message = message.replace(word, "")
    # Убираем лишние пробелы
    message = ' '.join(message.split())
    return message

@bot.message_handler(commands=['party'])
def add_user_to_party(message):
    user_id = message.from_user.id
    User = db_handler.Query()
    if not game_db.contains(User.user_id == user_id):
        game_db.insert({'user_id': user_id})
        bot.reply_to(message, f"вас будут тегать")
    else:
        bot.reply_to(message, f"уже в списке")

@bot.message_handler(commands=['noparty'])
def add_user_to_party(message):
    user_id = message.from_user.id
    User = db_handler.Query()
    if game_db.contains(User.user_id == user_id):
        game_db.remove({'user_id': user_id})
        bot.reply_to(message, f"вас не будут тегать")
    else:
        bot.reply_to(message, f"тебя и так не трогали")

@bot.message_handler(commands=['partyoff'])
def party_off(message):
    party_mode = False
    bot.reply_to(message, f"Режим теганья выключен")    

@bot.message_handler(commands=['partyon'])
def party_on(message):
    party_mode = True
    bot.reply_to(message, f"Режим теганья включен")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):        
    if not party_mode:
        return

    if not message.caption:
        return
    
    cleaned_message = clean_message(message.caption.lower())
    if cleaned_message in ["кто", "мы"]:
        user_ids = [user['user_id'] for user in game_db.all()]
        random_user_id = random.choice(user_ids)
        mention_link = f"tg://user?id={random_user_id}"
        bot.reply_to(message, f"[Тыкнул пальцем]({mention_link})!", parse_mode='Markdown')  